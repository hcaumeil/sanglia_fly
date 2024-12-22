FROM python:3.12.3-alpine

RUN apk add curl musl-dev gcc libpq-dev g++
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --profile minimal -y --default-toolchain 1.79
ENV PATH $PATH:/root/.cargo/bin

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "__main__.py"]
