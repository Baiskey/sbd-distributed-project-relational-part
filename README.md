## Prerequisites

Install docker and follow instructions from
`https://hackernoon.com/dont-install-postgres-docker-pull-postgres-bee20e200198`

Start Docker container with Postgres
`docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres`