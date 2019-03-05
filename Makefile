# Define filename references
DEV_FOLDER := docker/dev
DEV_COMPOSE_FILE := docker/dev/docker-compose.yml

# Set target lists
.PHONE: help

help:
	@echo ''
	@echo 'Usage:'
	@echo '${YELLOW} make ${RESET} ${GREEN}<target> [options]${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		message = match(lastLine, /^## (.*)/); \
		if (message) { \
			command = substr($$1, 0, index($$1, ":")-1); \
			message = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} %s\n", command, message; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''

build:
	@ echo "Building push service..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} up -d
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app ${DEV_FOLDER}/start_service.sh

status:
	@ echo "Checking status..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} ps

create:
	@ echo 'Creating $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} create $(service)

start:
	@ echo 'Starting  $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} start $(service)

run-app:
	@ echo 'Running mrm_api on port 5000...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app ${DEV_FOLDER}/start_service.sh

stop:
	@ echo 'Stopping $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} stop $(service)

restart:
	@ echo 'restarting $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} stop $(service)
	@ docker-compose -f ${DEV_COMPOSE_FILE} rm -f -v $(service)
	@ docker-compose -f ${DEV_COMPOSE_FILE} create --force-recreate $(service)
	@ docker-compose -f ${DEV_COMPOSE_FILE} start $(service)

test:
	@ echo 'start tests...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app ${DEV_FOLDER}/start_tests.sh "$(test)"

ssh:
	@ echo 'ssh...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec $(service) /bin/bash

down:
	@ echo "push service going down..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} down

services:
	@ echo "Getting services..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} ps --services

remove:
	@ echo "Removing $(service) container"
	@ docker-compose -f ${DEV_COMPOSE_FILE} rm -f -v $(service)

clean: down
	@ echo "Removing containers..."
	@ docker stop mrm_database mrm_api mrm_redis
	@ docker rm mrm_database mrm_api mrm_redis

kill:
	@ echo "killing..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} kill -s SIGINT
