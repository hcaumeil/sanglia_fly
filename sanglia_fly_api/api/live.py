from fastapi import FastAPI, Response, APIRouter, status
from fastapi.responses import StreamingResponse
import json
from contextlib import aclosing

from consumer import publisher, Subscriber
from models import LiveRecord

router = APIRouter()

async def _records_generator():
    subscriber = Subscriber()
    publisher.subscribe(subscriber)

    async def aclose():
        publisher.unsubscribe(subscriber)

    while True:
        r = await subscriber.get()
        if r != None:
            data: LiveRecord = r
            data = data.toJson()
            yield f"data: {data}\n"

async def records_generator():
    async with aclosing(_records_generator()) as values:
        async for value in values:
            yield value

@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    return StreamingResponse(records_generator(), media_type="text/event-stream")
