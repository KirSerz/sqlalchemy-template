# Template sqlalchemy-template + fastapi + admin panel

This guide covers setting up the project locally for development and testing purposes.

## Project Setup

### Virtual Environment

It's recommended to use a Python virtual environment to isolate dependencies:

```
python -m venv venv
. venv/bin/activate
```

### Environment Variables

Copy `.env.example` to `.env` and update any credentials, settings, etc.

### Install Dependencies

`pip install -r src/requirements.txt`

### Initialize Database

Create migrations from updated database schema:

`alembic revision --autogenerate -m "<migrations name>"`

Run migrations to setup database schema:

`alembic upgrade head`

###

## Start Local Development

### Start database and other services with docker

`docker-compose up -d`

### Run app

`uvicorn apps.main:app --reload`

### set PYTHONPATH for run app scripts
`
(.venv) ...\sqlalchemy-template> cd .\src\
(.venv) ...\sqlalchemy-template> $env:PYTHONPATH = "."
`

### Create superuser

`python apps/users/scripts/create_user.py -un admin -al 3 -pass adminpass`

### Useful URLs

- **Admin panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Swagger UI (API docs):** [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)
