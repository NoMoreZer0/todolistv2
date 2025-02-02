# Todolist v2

Just another todo list. Features:
* Scheduled tasks
* Push notifications


## Run the project

Project contains docker-compose in order to run it everywhere. Nevertheless, you can run it locally by installing needed components from docker locally.


### Run from docker

#### Create docker network

```shell
docker network create todolist_default
```

#### Build & Run the project

```shell
docker compose up --build -d
```
