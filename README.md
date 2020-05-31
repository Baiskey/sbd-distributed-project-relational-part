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

`cd mongodb-cluster-scripts`

`docker-compose up`

Open new terminal and then.. `cd mongodb-cluster-scripts`, `sh init.sh`

After some time do following..

`docker-compose exec router mongo`

`use test_database`

`sh.enableSharding("test_database")`

`sh.shardCollecton("test_database.person", {"pesel": 1} )`
`sh.shardCollecton("test_database.address", {"id": 1} )`

`sh.disableBalancing("test_database.address")`

`sh.addShardTag("shard01", "ALPHA")`
`sh.addShardTag("shard02", "BETA")`

`sh.addTagRange("test_database.address", {"id": 1}, {"id": 470}, "ALFA")`
`sh.addTagRange("test_database.address", {"id": 471}, {"id": 943}, "BETA")`

`sh.enableBalancing("test_database.person")`
`sh.enableBalancing("test_database.address")`

Then run script MongoDBImportData.py (it inserts data)

Then check if Address data is distributed to 3 MongoDB instances

`db.person.getShardDistribution()`
`db.address.getShardDistribution()`