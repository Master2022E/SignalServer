IMAGE_NAME=signal-server
CONTAINER_NAME=signal-server

all: run

logs:
	docker logs $(CONTAINER_NAME) -f

publish: tag
	docker push $(username)/$(IMAGE_NAME):latest

tag: build
	docker tag $(IMAGE_NAME) $(username)/$(IMAGE_NAME):latest

run: build
	docker run -d -p 8080:8080 --name $(CONTAINER_NAME) $(IMAGE_NAME):latest

build: clean_up
	docker build . -t $(IMAGE_NAME)

clean_up: stop
	docker rm $(CONTAINER_NAME)
	docker rmi $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)

local-install:
	python -m pip install -r requirements.txt

local-run:
	python -m flask run --host=0.0.0.0 --port=8080