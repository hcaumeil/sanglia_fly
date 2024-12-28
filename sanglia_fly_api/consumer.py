import asyncio

# https://github.com/dpkp/kafka-python/issues/2401
import sys
import six
import json

if sys.version_info >= (3, 12, 0):
    sys.modules["kafka.vendor.six.moves"] = six.moves
from kafka import KafkaConsumer

from db import db

class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def publish(self, message):
        for subscriber in self.subscribers:
            subscriber.receive(message)


class Subscriber:
    def __init__(self):
        self.queue = asyncio.Queue()

    def receive(self, message):
        try:
            self.queue.put_nowait(message)
        except Exception as e:
            print("e:" + str(e))

    async def get(self):
        return await self.queue.get()


publisher = Publisher()

from utils import expect_env_var
from models import LiveRecord

kafka_url = expect_env_var("KAFKA_URL")
kafka_topic = expect_env_var("KAFKA_TOPIC")


def main():
    while True:
        try:
            consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_url)

            for msg in consumer:
                cur = db.cursor()
                liveRecord = LiveRecord.fromJson(msg.value.decode("utf-8"))
                print(liveRecord)
                publisher.publish(liveRecord)
                cur.execute(
                    "INSERT INTO records (latitude,longitude,altitude,orientation,speed,type,origin) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                    (liveRecord.latitude,liveRecord.longitude,liveRecord.altitude,liveRecord.orientation,liveRecord.speed,liveRecord.type,liveRecord.origin)
                )
                db.commit()
                cur.close()
        except Exception as e:
            print("error in consumer : " + str(e))
                 
