import asyncio
import json
import random
from asyncio import create_task

import requests
from kafka import KafkaProducer

from sync import select_flight
from utils import expect_env_var
from utils import header_request

kafka_url = expect_env_var("KAFKA_URL")
kafka_topic = expect_env_var("KAFKA_TOPIC")


def get_flights():
    list_flights = requests.get('https://www.flightradar24.com/v1/search/web/find?query=afr&limit=5000',
                                headers=header_request())

    list_flights = list_flights.json()['results']

    live_flights = []
    for flight in list_flights:
        if flight['type'] == 'live':
            if flight['detail']['operator'] == 'AFR':
                live_flights.append(flight)

    print('nb live flight : ', len(live_flights))

    return live_flights


def on_send_success(record_metadata):
    print('topic : ', record_metadata.topic)
    print('partition : ', record_metadata.partition)
    print('offset : ', record_metadata.offset)


def on_send_error(excp):
    print('I am an errback', excp)


async def _main(selected_flight):
    # Create a producer with JSON serializer
    producer = KafkaProducer(
        bootstrap_servers=kafka_url,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        max_block_ms=3000,
    )

    while True:
        data_flight = requests.get(
            'https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=' + selected_flight['id'],
            headers=header_request())
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

        print(data)
        # Sending JSON data
        producer.send(topic=kafka_topic, value=data).add_callback(on_send_success).add_errback(on_send_error)

        await asyncio.sleep(31 + random.random() * 8)


# producer.flush()


async def main():
    live_flights = get_flights()
    selected_flight, sync_task = await select_flight(kafka_url, "sync", live_flights)

    main_task = create_task(_main(selected_flight))

    await main_task
    await sync_task


asyncio.run(main())
