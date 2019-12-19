.PHONY: build build-db build-server build-router build-client build-c2 save


build: build-db build-server build-router build-client build-c2

build-db: db/Dockerfile db/dump.sql
	docker build -q -t cs4404m3t9/db -f db/Dockerfile db

build-server: server/Dockerfile $(wildcard server/server/**/*)
	docker build -q -t cs4404m3t9/ws -f server/Dockerfile server

build-router: $(wildcard router/**/*)
	docker build -q -t cs4404m3t9/router -f router/Dockerfile router 

build-client: client/Dockerfile client/client.sh
	docker build -q -t cs4404m3t9/client -f client/Dockerfile client

build-c2: c2/Dockerfile c2/cookie.txt c2/run_command.py
	docker build -q -t cs4404m3t9/c2 -f c2/Dockerfile c2


save: target/db-image.tar target/server-image.tar target/router-image.tar

target/db-image.tar: build-db 
	docker save --output target/db-image.tar cs4404m3t9/db

target/server-image.tar: build-server 
	docker save --output target/server-image.tar cs4404m3t9/ws

target/router-image.tar: build-router
	docker save --output target/router-image.tar cs4404m3t9/router

# TODO: Add saves for other images if we want to deploy that way. We could also build on target

target/containernet-master.tar.gz:
	wget https://github.com/containernet/containernet/archive/master.tar.gz -O target/containernet-master.tar.gz