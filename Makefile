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

# This command starts the application in dev mode 
dev:
	fastapi dev src/

# This command starts the application in prod mode 
run:
	fastapi run src/

.PHONY: install-docker postgresql dev run
