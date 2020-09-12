SSH_PORT=22000
IMAGE=tfm.img
CONTAINER=tfm.con
EXEC=docker exec -it $(CONTAINER)
EXEC_U=docker exec -itu $$(id -u) $(CONTAINER)
ENV_PATH=/app/.env

stop:
		# Always true to avoid an error if container does not exist.
		docker rm -f $(CONTAINER) || true
build:
		docker build -t $(IMAGE) .

start: stop build
		# Run container in the background.
		docker run -v $(PWD):/app -w /app -p $(SSH_PORT):22 --name $(CONTAINER) -di $(IMAGE)
		# Create user app as the current user (same id).
		$(EXEC) useradd -s /bin/bash -u $$(id -u) -Md /app app
		$(EXEC) /bin/bash -c "echo app:app | chpasswd"
		# Ssh service cannot be started from the docker image.
		$(EXEC) service ssh start
		# Conda local environment.
		$(EXEC_U) conda create pip --prefix $(ENV_PATH) -y

root:
		$(EXEC) /bin/bash -l

ssh:
		# Asks for password: app. Avoid having ssh key issues.
		ssh -o PubkeyAuthentication=no app@localhost -p $(SSH_PORT)

conda:
		$(EXEC_U) conda $(filter-out $@,$(MAKECMDGOALS)) --prefix $(ENV_PATH)

pip:
		$(EXEC_U) $(ENV_PATH)/bin/pip $(filter-out $@,$(MAKECMDGOALS))

