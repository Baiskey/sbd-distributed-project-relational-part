## Prerequisites

Install docker and follow instructions from
`https://hackernoon.com/dont-install-postgres-docker-pull-postgres-bee20e200198`

Start Docker container with Postgres
`docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres`

Start Docker with MongoDB
`docker pull mongo`
`docker run --rm -d -p 27017-27019:27017-27019 --name mongodb mongo`