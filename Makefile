BACK_SERVICE := smart-api
BASE_SERVICE := baseImage
ROOT_DIR := $(shell pwd)
BLUE = \033[34m
NC = \033[0m


.PHONY: help build build-base build-back build-all

help: ## Show help message
	@printf "Usage:\n"
	@printf "  make $(BLUE)<target>$(NC)\n\n"
	@printf "Targets:\n"
	@perl -nle'print $& if m{^[a-zA-Z0-9_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; \
		{printf "$(BLUE)  %-18s$(NC) %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

# DOCKER TASKS
## build
build: build-back ## Build the container

build-all: build-base build-back ## build base and back

build-base: ## Build backend base image
	docker-compose build --force-rm --no-cache $(BASE_SERVICE)

build-back: ## Build backend image
	docker-compose build --force-rm --no-cache $(BACK_SERVICE)

build-push: build-back ## push ${BACK_SERVICE} to docker hub
	docker-compose push $(BACK_SERVICE)