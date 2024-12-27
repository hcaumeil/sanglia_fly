import json
import random
import uuid
from asyncio import create_task, sleep

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


def exclude_flight(fid, flights, excluded):
    for i in range(0, len(flights)):
        if flights[i]["id"] == fid:
            flights.pop(i)
            break
    if fid not in excluded:
        excluded.append(fid)


async def receive_messages(consumer, timeout):
    messages = []

    async def _receive_messages():
        async for message in consumer:
            if message.value["type"] != "":
                messages.append(message.value)

    task = create_task(_receive_messages())

    await sleep(timeout)

    task.cancel()

    return messages


async def _select_flight(consumer, producer, kafka_topic, flights, excluded):
    # Select a random flight
    flight = random.choice(flights)

    # Listen for [0.5s; 5s] for FlightsMessage and FlightMessage
    timeout = random.random() * 4.5 + 0.5
    messages = await receive_messages(consumer, timeout)

    # Remove flights from the list, if the selected flight is in, restart from the select step
    restart = False
    for message in messages:
        if message["type"] == "Flight":
            exclude_flight(message["id"], flights, excluded)
            if message["id"] == flight["id"]:
                print("Someone got same id as me", flight["id"], flush=True)
                restart = True
        elif message["type"] == "Flights":
            for f in message["ids"]:
                exclude_flight(f, flights, excluded)
                if f == flight["id"]:
                    print("Someone got same id as me", flight["id"], flush=True)
                    restart = True
    if restart:
        return await _select_flight(consumer, producer, kafka_topic, flights, excluded)

    # Send FlightMessage
    await producer.send_and_wait(topic=kafka_topic, value={"type": "Flight", "id": flight["id"]})

    return flight


# Listen for JoinMessage and sends selected flights
async def _task(consumer, producer, kafka_topic, excluded):
    async for message in consumer:
        message = message.value
        if message["type"] == "Flight":
            if message["id"] not in excluded:
                excluded.append(message["id"])
        elif message["type"] == "Flights":
            for fid in message["ids"]:
                if fid not in excluded:
                    excluded.append(fid)
        elif message["type"] == "Join":
            await producer.send_and_wait(topic=kafka_topic, value={"type": "Flights", "ids": excluded})


async def select_flight(kafka_url, kafka_topic, flights):
    print("Selecting flight...", flush=True)

    excluded = []

    myid = str(uuid.uuid4())
    print("My id is ", myid, flush=True)

    def deserializer(v):
        m = json.loads(v.decode('utf-8'))
        if m["node_id"] == myid:
            m["type"] = ""
        return m

    def serializer(v):
        v["node_id"] = myid
        return json.dumps(v).encode('utf-8')

    consumer = AIOKafkaConsumer(kafka_topic, bootstrap_servers=kafka_url, value_deserializer=deserializer,
                                group_instance_id=myid, max_poll_interval_ms=300)
    await consumer.start()
    producer = AIOKafkaProducer(bootstrap_servers=kafka_url, value_serializer=serializer,
                                partitioner=lambda key_bytes, all_partitions, available_partitions: 0)
    await producer.start()

    # Send JoinMessage
    await producer.send_and_wait(topic=kafka_topic, value={"type": "Join"})

    # Listens for 3s for FlightsMessage and FlightMessage
    messages = await receive_messages(consumer, 5)

    # Remove flights from the list
    for message in messages:
        if message["type"] == "Flight":
            exclude_flight(message["id"], flights, excluded)
        elif message["type"] == "Flights":
            for flight in message["ids"]:
                exclude_flight(flight, flights, excluded)

    selected = await _select_flight(consumer, producer, kafka_topic, flights, excluded)

    print("Selected flight: ", selected["id"], flush=True)

    task = create_task(_task(consumer, producer, kafka_topic, excluded))

    return selected, task
