COMPOSE = @docker-compose
ROOT_DIR := $(shell pwd)
BLUE = \033[34m
NC = \033[0m


.PHONY: help up down init-db

help: ## Show help message
	@printf "Usage:\n"
	@printf "  make $(BLUE)<target>$(NC)\n\n"
	@printf "Targets:\n"
	@perl -nle'print $& if m{^[a-zA-Z0-9_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; \
		{printf "$(BLUE)  %-18s$(NC) %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

## build image
build: ## build
	$(COMPOSE) build


## Run containers
up: ## start
	$(COMPOSE) up


## Stop containers
down: ## stop
	$(COMPOSE) down


## init db
init-db: ## remove db volumes
	$(COMPOSE) down --volumes
