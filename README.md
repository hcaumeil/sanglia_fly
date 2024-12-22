# Sanglia Fly


## Docker

The components of Sanglia Fly are dockerized.

Each component has its own docker compose file to make it usable on different hosts.

In addition, a docker compose file with all components exists to make the development and testing process easier.

The different components use docker compose watch feature to reload the corresponding services.

### Starting Kafka broker

```shell
cd docker
docker compose -f kafka.compose.yml up
```

### Starting the API

```shell
cd docker
docker compose -f api.compose.yml up

# With watch mode
docker compose -f api.compose.yml up --watch
```

### Starting the components

```shell
cd docker
docker compose -f all.compose.yml up

# With watch mode
docker compose -f all.compose.yml up --watch
```
