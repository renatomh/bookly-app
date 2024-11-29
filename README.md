<h1 align="center"><img alt="FastAPI Beyond CRUD" title="FastAPI Beyond CRUD" src=".github/logo.png" width="250" /></h1>

# FastAPI Beyond CRUD

## 💡 Project's Idea

This project was developed to create a REST API for a book review web service, using FastAPI.

## 🔍 Features

- Signup and login to the application
- Create and manage books
- Review the existing books
- Add tags to the books

## 🛠 Technologies

During the development of this project, the following techologies were used:

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Flower](https://flower.readthedocs.io/en/latest/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Schemathesis](https://schemathesis.readthedocs.io/en/stable/)
- [Alembic (Migrations)](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy (ORM)](https://www.sqlalchemy.org/)
- [Black Formatter](https://github.com/psf/black)

## 💻 Project Configuration

Note: the project was developed with Python version **3.9.13**.

### First, create a new virtual environment on the root directory

```bash
$ python -m venv env
```

### Activate the created virtual environment

```bash
$ .\env\Scripts\activate # On Windows machines
$ source ./env/bin/activate # On MacOS/Unix machines
```

### Install the required packages/libs

```bash
(env) $ pip install -r requirements.txt
```

### Creating config files

Create an _.env_ file on the root directory, with all needed variables, credentials and API keys, according to the sample provided (_[example.env](./example.env)_).

### Setting up the databases

Run the command below to create the PostgreSQL and Redis databases locally in your machine (you should have Docker installed, there's also a Make command for that):

```bash
make postgresql
make redis
```

## 💾 Database Migrations

Once the SQL server is ready and the required credentials to access it are present in the _.env_ file, you can run the migrations with the command:

```bash
(env) $ alembic upgrade head
```

You can also downgrade the migrations with the following command:

```bash
(env) $ alembic downgrade base
```

Alternatively, you can migrate up or down by a specific number of revision, or to a specific revision:

```bash
(env) $ alembic upgrade +2 # Migrating up 2 revisions
(env) $ alembic downgrade -1 # Migrating down 1 revision
(env) $ alembic upgrade db9257fac0e2 # Migrating to a specific revision
```

To generate new revisions for the migrations, when there are changes to the application models or new ones are created, you should import any new models in the [migrations/env.py](./migrations/env.py#L12) file, and then run the command below (where you can provide a custom short description for the update):

```bash
(env) $ alembic revision --autogenerate -m "revision description"
```

## ⏯️ Running

To run the project in a development environment, execute the following commands on the root directory, with the virtual environment activated.

```bash
(env) $ make dev
(env) $ make celery  # In another terminal
(env) $ make flower  # In another terminal, for Celery tasks monitoring
```

In order to leave the virtual environment, you can simply execute the command below:

```bash
(env) $ deactivate
```

## 🧪 Testing

In order to make sure that the application's main features are working as expected, some tests were created to assert the functionalities.

To allow the execution of the tests, first the required dependencies must be installed:

```bash
(env) $ pip install -r requirements-test.txt
```

The tests can then be run:

```bash
(env) $ make test
```

Also, you can use Schemathesis to run tests automatically generated from an OpenAPI specification:

```bash
(env) $ make schemathesis
```

### Documentation:

- [FastAPI Beyond CRUD Full Course - A FastAPI Course](https://youtu.be/TO4aQ3ghFOc?si=9fiydpdBQxgfhlgy)
- [FastAPI Beyond CRUD](https://jod35.github.io/fastapi-beyond-crud-docs/site/)
- [How to generate an app password](https://support.google.com/mail/thread/205453566?hl=en&msgid=208526631)

## 📄 License

This project is under the **MIT** license. For more information, access [LICENSE](./LICENSE).
