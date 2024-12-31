from api import main as api_main
from consumer import main as consumer_main

import asyncio
import time


async def main():
    async with asyncio.TaskGroup() as tg:
        kafka = tg.create_task(consumer_main())
        api = tg.create_task(api_main())

        print(f"started at {time.strftime('%X')}")
    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
