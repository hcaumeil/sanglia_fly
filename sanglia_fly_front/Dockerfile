FROM node:18 AS builder

COPY . /app
WORKDIR /app
RUN npm install
ARG VITE_API_URL
RUN npm run build

FROM python:3.12.3-alpine

RUN apk add curl

COPY --from=builder /app/dist /app
WORKDIR /app

ENTRYPOINT ["python", "-m", "http.server"]
