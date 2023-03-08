.PHONY: all
all: py3/bin/pip3

py3/bin/pip3: requirements.txt
	python3 -m venv py3
	pip install -IUr requirements.txt


fg:
	docker-compose up

start:
	docker-compose up -d

stop:
	docker-compose down
