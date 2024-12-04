from fastapi import FastAPI, Response, APIRouter, status
from fastapi.responses import StreamingResponse
import json

from consumer import publisher, Subscriber
from models import LiveRecord

router = APIRouter()


async def records_generator():
    subscriber = Subscriber()
    publisher.subscribe(subscriber)

    for r in iter(subscriber.get, None):
        print(r)
        if r != None:
            data: LiveRecord = r
            data = data.toJson()
            yield f"data: {data}\n"

    publisher.unsubscribe(subscriber)


@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    return StreamingResponse(records_generator(), media_type="text/event-stream")
