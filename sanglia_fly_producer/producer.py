import asyncio
import json
import random
from asyncio import create_task

import requests
from aiokafka import AIOKafkaProducer

from utils import env_var_or_false
from sync import select_flight
from utils import expect_env_var
from utils import header_request

kafka_url = expect_env_var("KAFKA_URL")
kafka_topic = expect_env_var("KAFKA_TOPIC")

restart_when_finished = env_var_or_false("RESTART_WHEN_FINISHED")


def get_flights():
    list_flights = requests.get('https://www.flightradar24.com/v1/search/web/find?query=afr&limit=5000',
                                headers=header_request())

    list_flights = list_flights.json()['results']

    live_flights = []
    for flight in list_flights:
        if flight['type'] == 'live':
            if flight['detail']['operator'] == 'AFR':
                live_flights.append(flight)

    print('nb live flight : ', len(live_flights), flush=True)

    return live_flights


async def _main(selected_flight, sync_task):
    # Create a producer with JSON serializer
    producer = AIOKafkaProducer(
        bootstrap_servers=kafka_url,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )
    await producer.start()

    session = requests.sessions.Session()
    last_data = None
    headers = header_request()

    while True:
        data_flight = session.get(
            'https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=' + selected_flight['id'],
            headers=headers)
        data_flight = data_flight.json()

        if not data_flight['status']['live']: break

        selected_data_flight = data_flight["trail"][0]

        data = {
            'origin': selected_flight['detail']['callsign'],
            'latitude': selected_data_flight['lat'],
            'longitude': selected_data_flight['lng'],
            'altitude': selected_data_flight['alt'] * 0.3048,
            'orientation': selected_data_flight['hd'],
            'speed': selected_data_flight['spd'],
            'type': selected_flight['detail']['ac_type'],
        }

        if last_data is not None and data == last_data:
            print("Recreating session", flush=True)
            session.close()
            session = requests.sessions.session()
            last_data = None
            headers = header_request()
        else:
            last_data = data

        print(data, flush=True)
        # Sending JSON data
        await producer.send_and_wait(topic=kafka_topic, value=data)

        await asyncio.sleep(31 + random.random() * 8)

    sync_task.cancel()


# producer.flush()


async def main():
    while True:
        live_flights = get_flights()
        selected_flight, sync_task = await select_flight(kafka_url, "sync", live_flights)

        main_task = create_task(_main(selected_flight, sync_task))

        await main_task
        await sync_task
        if not restart_when_finished: break


asyncio.run(main())
