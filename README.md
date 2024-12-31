# Sanglia Fly

## Components

### Kafka broker

This component is the core of communications between producers and the API.
Since the docker service uses the host network, it requires no specific configuration

### API

FastAPI getting locations sent through the Kafka broker by the producers and saving them to a db and streaming them with
Server-Sent Events.

The environment variable `KAFKA_URL` found in `docker/api.compose.yml` should be replaced by the Kafka broker IP and
port (e.g. `10.36.0.28:9092`).

The API exposes the port `8080`.

### Producer

The producer gets live flights operated by Air France from [flightradar24.com](https://www.flightradar24.com).
The list of live flights is generally limited to 25 (the "API" of flightradar24 doesn't seem to support paging).
Then by using the free API, we can only get an update every 30 seconds by live flight.
So when tracking a flight, we will produce a new coordinate every 30 seconds.

To note that we replaced the ip information sent through Kafka by the flight identifier.

Multiple producers will try to synchronize through the `sync` topic by using a very dumb version of the election
algorithm of the [Raft](https://raft.github.io/) consensus algorithm.
The algorithm will fail if the ~25 flights are already taken by other producers.

Like the API, the environment variable `KAFKA_URL` found in `docker/producer.compose.yml` should be replaced by the
Kafka broker IP and port (e.g. `10.36.0.28:9092`).

#### Environment variables

`RETRY_ON_KAFKA_INIT_ERR`: (bool) when `true` the producer while continues to try to initialize if the broker is
unreachable.

`RESTART_WHEN_FINISHED`: (bool) enable a producer to choose another flight when the previous finished.

### Front

What will be the project without a frontend?
The front wrote in [Vue.js](https://vuejs.org/) permits 2d or 3d visualization.

A build time environment variable can be supplied to specify the API location in `front.compose.yml` (
`services.front.build.args`): `VITE_API_URL` (e.g. `http://10.36.0.28:8080`).

The frontend exposes the port `8000`.

## Notes on the dockerization

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

### Starting the producer

```shell
cd docker
docker compose -f producer.compose.yml up

# With watch mode
docker compose -f producer.compose.yml up --watch
```

#### Scaling producers

```shell
docker compose -f producer.compose.yml scale producer=N # Where N is the number of producers
```

### Starting the frontend

```shell
cd docker
docker compose -f front.compose.yml up

# With watch mode
docker compose -f front.compose.yml up --watch
```

### Starting the components

```shell
cd docker
docker compose -f all.compose.yml up

# With watch mode
docker compose -f all.compose.yml up --watch
```

#### Scaling producers

```shell
docker compose -f all.compose.yml scale producer=N # Where N is the number of producers
```

## FAQ

### I want to start 2 producers, the Kafka broker, the API and the frontend on different machines

_Make sure that at least the producers, Kafka broker and the API are in the same network.
Otherwise, the setup is left as an exercise for the reader._

Put the project on your machines and go to the `docker` folder.

On the machine with `IP1`, start the Kafka broker by running:

```shell
docker compose -f kafka.compose.yml up
```

On the machine with `IP2`, replace the value `todo` for the environment variable `KAFKA_URL` by `IP1:9092`
in [producer.compose.yml](docker/producer.compose.yml).
Then run:

```shell
docker compose -f producer.compose.yml up
```

On the machine with `IP3`, replace the value `todo` for the environment variable `KAFKA_URL` by `IP1:9092`
in [producer.compose.yml](docker/producer.compose.yml).
Then run:

```shell
docker compose -f producer.compose.yml up
```

On the machine with `IP4`, replace the value `todo` for the environment variable `KAFKA_URL` by `IP1:9092`
in [api.compose.yml](docker/api.compose.yml).
Then run:

```shell
docker compose -f api.compose.yml up
```

On the machine with `IP5`, replace the value `http://localhost:8080` for the build argument `VITE_API_URL` by
`http://IP4:8080` in [front.compose.yml](docker/front.compose.yml).
Then run:

```shell
docker compose -f front.compose.yml up
```

Finally, go to http://IP5:8000/ and voilà.


### I want to start 5 producers, the Kafka broker, the API and the frontend on the same machine

Put the project on your machine and go to the `docker` folder.

Just do:

```shell
docker compose -f all.compose.yml up

# And on a different shell
docker compose -f all.compose.yml scale producer=5
```

### You have a CI?

Yes, we deploy all the components on the cloud ☁️.
You might have received a link in your PM, if not, that's bad for you.
