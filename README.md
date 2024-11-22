<h1 align="center"><img alt="FastAPI Beyond CRUD" title="FastAPI Beyond CRUD" src=".github/logo.png" width="250" /></h1>

# FastAPI Beyond CRUD

## 💡 Project's Idea

This project was developed to create a REST API for a book review web service, using FastAPI.

## 🔍 Features

-

## 🛠 Technologies

During the development of this project, the following techologies were used:

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)

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

Create an _.env_ file on the _src_ directory, with all needed variables, credentials and API keys, according to the sample provided (_[example.env](./src/example.env)_).

### Setting up the database

Run the command below to create the PostgreSQL database locally in your machine (you should have Docker installed, there's also a Make command for that):

```bash
make postgresql
```

## ⏯️ Running

To run the project in a development environment, execute the following command on the root directory, with the virtual environment activated.

```bash
(env) $ make dev
```

In order to leave the virtual environment, you can simply execute the command below:

```bash
(env) $ deactivate
```

### Documentation:

- [FastAPI Beyond CRUD Full Course - A FastAPI Course](https://youtu.be/TO4aQ3ghFOc?si=9fiydpdBQxgfhlgy)
- [FastAPI Beyond CRUD](https://jod35.github.io/fastapi-beyond-crud-docs/site/)

## 📄 License

This project is under the **MIT** license. For more information, access [LICENSE](./LICENSE).
