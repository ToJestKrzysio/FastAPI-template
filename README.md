# FastAPI microservice template

## Setup

* Copy all `envs/<name>-default.env` files renaming them to `env/<name>.env`.
* Fill missing environment variables in renamed files.
* Check volumes used by docker compose, if necessary update them.
* start docker containers using docker compose `docker compose up`.

## File structure

```text
├── api/   
│   ├── dependencies.py - generic dependencies for api endpoints
│   └── main.py - entrypoint to fastAPI application 
├── db/
│   ├── alembic/
│   │   ├── versions/ - directory with alembic migrations
│   │   ├── env.py - runtime configuration of alembic
│   │   └── script.py.mako - migration file template
│   ├── tests/ 
│   │   └── conftest.py - fixtures for module tests
│   ├── alembic.ini - alembic configuration file
│   ├── config.py - configuration of the Database connector
│   ├── models.py - Pydantic models of the data
│   └── repositories.py - Repositories used to access data in db.
└── envs/ - directory containing env files used for docker compose
```
