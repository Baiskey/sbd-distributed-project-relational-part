## Prerequisites

Install docker and follow instructions from
`https://hackernoon.com/dont-install-postgres-docker-pull-postgres-bee20e200198`

Start Docker container with Postgres
`docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres`

Start Docker with MongoDB
`docker pull mongo`
`docker run --rm -d -p 27017-27019:27017-27019 --name mongodb mongo`

Deletion of all stopped containers
`docker rm $(docker ps -a -q)`

Stopping Docker container with MongoDB
`docker stop mongodb`

Stopping all containers
`docker rm $(docker ps -a -q)`

### Sharding MongoDB ###

`docker-compose exec router mongo`

`use admin`

`sh.enableSharding("test_database")`

`sh.shardCollecton("test_database.person", {"pesel": 1} )`
`sh.shardCollecton("test_database.address", {"id": 1} )`

`db.runCommand({"updateZoneKeyRange": "test_database.address", min: {"id": 1}, max: {"id": 200}, zone: "alpha" })`

`sh.enableBalancing("test_database.person")`
`sh.enableBalancing("test_database.address")`
`sh.startBalancer()`

Then run script MongoDBImportData.py

`db.person.getShardDistribution()`
`db.address.getShardDistribution()`



