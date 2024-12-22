import uvicorn

from fastapi import FastAPI, Request, status
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from utils import expect_env_var

port = expect_env_var("PORT")

from .error import ErrorResponse, ErrorKind
from .records import router as records_router
from .live import router as live_router
from db import db

app = FastAPI()

# Cors ff
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.db = db

app.include_router(records_router, prefix="/records")
app.include_router(live_router, prefix="/live")


@app.get("/")
def root() -> Response:
    return Response()


@app.get("/ping")
def ping():
    return "PONG!"


@app.get("/teapot", status_code=status.HTTP_418_IM_A_TEAPOT)
def teapot():
    return "I am a teapot"


async def main():
    config = uvicorn.Config(app, port=int(port), host="0.0.0.0")
    server = uvicorn.Server(config)
    await server.serve()
