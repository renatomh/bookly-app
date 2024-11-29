# Including environment variables to the makefile
include .env

# This command installs Docker in a Linux Ubuntu machine
install-docker:
	sudo apt update
	sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	echo "deb [signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt update
	sudo apt install -y docker-ce
	sudo systemctl start docker
	sudo systemctl enable docker
	docker --version

# This command creates a PostgreSQL container
postgresql:
	docker run --name postgres-bookly -p ${SQL_PORT}:5432 -e POSTGRES_USER=${SQL_USER} -e POSTGRES_PASSWORD=${SQL_PASS} -e POSTGRES_DB=${SQL_DB} -v pgdata:/var/lib/postgresql/data -d postgres:15-alpine

# This command creates a Redis container
redis:
	docker run --name redis-bookly -p ${REDIS_PORT}:6379 -v redisdata:/data -d redis:7-alpine

# This command runs the required migrations up for the database
migrateup:
	alembic upgrade head

# This command downgrades all migrations on the database
migratedown:
	alembic downgrade base

# This command tests the app, setting up deprecation warnings and logging options
test:
	pytest -W ignore::DeprecationWarning -v -p no:logging

# This command generates and run tests based on an OpenAPI specification
schemathesis:
	schemathesis run http://localhost:8000/openapi.json --checks all --experimental=openapi-3.1

# This command starts the Celery app worker
celery:
	celery -A src.celery_tasks.c_app worker

# This command starts the Celery app flower monitoring tool
flower:
	celery -A src.celery_tasks.c_app flower

# This command starts the application in dev mode 
dev:
	fastapi dev src/

# This command starts the application in prod mode 
run:
	fastapi run src/

.PHONY: install-docker postgresql redis migrateup migratedown test schemathesis celery flower dev run
