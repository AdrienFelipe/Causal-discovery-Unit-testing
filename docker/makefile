SSH_PORT=22000
IMAGE=tfm.img
CONTAINER=tfm.con
EXEC=docker exec -it $(CONTAINER)

stop:
		docker rm -f $(CONTAINER) || true
build:
		docker build -t $(IMAGE) .

start: stop build
		docker run -v $(PWD):/app -p $(SSH_PORT):22 --name $(CONTAINER) -di $(IMAGE)
		$(EXEC) useradd -s /bin/bash -u $$(id -u) -Md /app app
		$(EXEC) /bin/bash -c "echo app:app | chpasswd"
		$(EXEC) service ssh start

root:
		$(EXEC) /bin/bash -l

ssh:
		ssh -o PubkeyAuthentication=no app@localhost -p $(SSH_PORT)
