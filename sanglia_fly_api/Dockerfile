FROM python:3.12.3-alpine

RUN apk add curl musl-dev gcc libpq-dev g++

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "__main__.py"]
