export

SHELL = /bin/bash
PYTHON = python3
PIP = pip3
LOG_LEVEL = INFO
PYTHONIOENCODING=utf8

# pytest args. Set to '-s' to see log output during test execution, '--verbose' to see individual tests. Default: '$(PYTEST_ARGS)'
PYTEST_ARGS =

# Docker container tag
DOCKER_TAG = 'ocrd/olahd-client'

# BEGIN-EVAL makefile-parser --make-help Makefile

help:
	@echo ""
	@echo "  Targets"
	@echo ""
	@echo "    deps       Install python deps via pip"
	@echo "    deps-test  Install testing python deps via pip"
	@echo "    install    Install"
	@echo "    docker     Build docker image"
	@echo "    test       Run unit tests"
	@echo "    coverage   Run unit tests and determine test coverage"
	@echo ""
	@echo "  Variables"
	@echo ""
	@echo "    PYTEST_ARGS  pytest args. Set to '-s' to see log output during test execution, '--verbose' to see individual tests. Default: '$(PYTEST_ARGS)'"
	@echo "    DOCKER_TAG   Docker container tag"

# END-EVAL

# Install python deps via pip
deps:
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

# Install testing python deps via pip
deps-test:
	$(PIP) install -U pip
	$(PIP) install -r requirements_test.txt

# Install
install:
	$(PIP) install -U pip
	$(PIP) install .

# Install-develop
install-dev:
	$(PIP) install -U pip
	$(PIP) install -e .

# Build docker image
docker:
	docker build -t $(DOCKER_TAG) .

# Run unit tests
test: tests/assets
	# declare -p HTTP_PROXY
	$(PYTHON) -m pytest --continue-on-collection-errors tests $(PYTEST_ARGS)

.PHONY: tests/assets
tests/assets:
	mkdir -p tests/assets
	cp -r repo/assets/data/* tests/assets

# Run unit tests and determine test coverage
coverage:
	coverage erase
	make test PYTHON="coverage run"
	coverage report
	coverage html

.PHONY: test install deps deps-test help
