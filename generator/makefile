# Container SSH port
SSH_PORT=22000
# Container Jupyter port
JUPYTER_PORT=22001
# Image and container tags (Causal Discovery Unit Testing)
IMAGE=cdut.img
CONTAINER=cdut.con
# Python virtual environment relative path
ENV_PATH=.env
# Path to the evaluation script
SCRIPT_PATH=src/discovery/evaluate.py
# Execute container as root
EXEC=docker exec -it $(CONTAINER)
# Execute container as current user
EXEC_U=docker exec -itu $$(id -u) $(CONTAINER)


stop:
		# Remove container instead of stopping it to free up its tag.
		# Always true to ignore error when container does not exist.
		docker rm -f $(CONTAINER) || true

build:
		docker build -t $(IMAGE) -f dockerfile .

create:
		$(EXEC_U) conda env create -f environment.yml --force --prefix $(ENV_PATH)

start: stop build
		# Run container in the background.
		docker run -v $(PWD):/app -w /app -p $(SSH_PORT):22 -p $(JUPYTER_PORT):$(JUPYTER_PORT) --name $(CONTAINER) -di $(IMAGE)
		# Create user 'app' as current user (same id).
		$(EXEC) useradd -s /bin/bash -u $$(id -u) -Md /app app
		$(EXEC) /bin/bash -c "echo app:app | chpasswd"
		# Start ssh service here, as it cannot be started from the docker image.
		$(EXEC) service ssh start
		# Remove previous SSH key.
		#ssh-keygen -f "$(HOME)/.ssh/known_hosts" -R "[localhost]:$(SSH_PORT)"
		# Create conda local environment only once.
		if [ ! -d "$(ENV_PATH)" ]; then make create; fi
		# Make environment Python available in PATH.
		$(EXEC) ln -fs /app/$(ENV_PATH)/bin/python /usr/bin/

root:
		$(EXEC) /bin/bash -l

ssh:
		# Asks for password: app. Avoid having ssh key issues.
		ssh -o PubkeyAuthentication=no app@localhost -p $(SSH_PORT)

conda:
		$(EXEC_U) conda $(filter-out $@,$(MAKECMDGOALS)) --prefix $(ENV_PATH)

pip:
		$(EXEC_U) $(ENV_PATH)/bin/pip $(filter-out $@,$(MAKECMDGOALS))

test:
		$(EXEC_U) bash -c "PYTHONPATH=src python -m unittest"

jupyter:
		# Use the link by IP, not by container name, unless you have it mapped to your local DNS
		$(EXEC_U) bash -c "PYTHONPATH=src $(ENV_PATH)/bin/jupyter $(filter-out $@,$(MAKECMDGOALS)) --ip=0.0.0.0 --port=$(JUPYTER_PORT) --no-browser"

evaluate:
		$(EXEC_U) bash -c "PYTHONPATH=src python $(SCRIPT_PATH)"
