#!/usr/bin/env bash
set -m

GREEN='\033[0;32m'
RESET='\033[0m'

/etc/kafka/docker/run&

while ! /opt/kafka/bin/kafka-metadata-quorum.sh --bootstrap-controller localhost:9093 describe --status 2> /dev/null || false; do
  sleep 0.2
done

echo -e "${GREEN}Kafka up${RESET}"

/usr/bin/httpd2&

/opt/kafka/bin/kafka-topics.sh --create --topic locations --bootstrap-server localhost:9092 --replication-factor 1 || true
/opt/kafka/bin/kafka-topics.sh --create --topic sync --bootstrap-server localhost:9092 --replication-factor 1 || true

fg
