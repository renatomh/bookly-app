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

# This command starts the application in dev mode 
dev:
	fastapi dev main.py

# This command starts the application in prod mode 
run:
	fastapi run main.py

.PHONY: install-docker dev run
