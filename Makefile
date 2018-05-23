all: build run

build:
	docker build . -t visitey_server

run:
	docker run visitey_server
