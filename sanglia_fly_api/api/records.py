from fastapi import APIRouter, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime

from .error import ErrorResponse, ErrorKind


class RecordOutput(BaseModel):
    at: datetime
    latitude: float
    longitude: float
    altitude: float
    orientation: int
    speed: float
    type: str


router = APIRouter()


def fetch_all_origins(db):
    cur = db.cursor()
    cur.execute("SELECT DISTINCT origin FROM records;")
    origins = cur.fetchall()
    db.commit()
    cur.close()
    return [o[0] for o in origins]


def origin_exist(db, origin: str):
    cur = db.cursor()
    cur.execute("SELECT 1 FROM records WHERE origin = %s;", (origin,))
    exists = cur.fetchone()
    cur.close()
    return exists


def fetch_records(db, origin: str):
    cur = db.cursor()
    cur.execute(
        "SELECT received_at,latitude,longitude,altitude,orientation,speed,type FROM records;"
    )
    records = cur.fetchall()
    db.commit()
    cur.close()
    return [
        RecordOutput(
            at=r[0],
            latitude=r[1],
            longitude=r[2],
            altitude=r[3],
            orientation=r[4],
            speed=r[5],
            type=r[6],
        )
        for r in records
    ]


@router.get("/", status_code=status.HTTP_200_OK)
def get_origins(req: Request):
    db = req.app.state.db

    try:
        origins = fetch_all_origins(db)
        return JSONResponse(content=jsonable_encoder(origins))
    except Exception as e:
        raise HTTPException(
            content=jsonable_encoder(
                ErrorResponse(
                    error="Internal error", error_kind=ErrorKind.internal_error
                )
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/{origin}", status_code=status.HTTP_200_OK)
def get_origins(req: Request, origin: str):
    db = req.app.state.db

    try:
        exist = origin_exist(db, origin)
        if not exist:
            return JSONResponse(
                content=jsonable_encoder(
                    ErrorResponse(
                        error="No records for this origin",
                        error_kind=ErrorKind.not_found,
                    )
                ),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        records = fetch_records(db, origin)
        return JSONResponse(content=jsonable_encoder(records))
    except Exception as e:
        raise HTTPException(
            content=jsonable_encoder(
                ErrorResponse(
                    error="Internal error", error_kind=ErrorKind.internal_error
                )
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
