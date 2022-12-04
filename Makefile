.ONESHELL:

.PHONY: clean install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	virtualenv -p python3.8 venv; \
	. venv/bin/activate; \
	pip install -r requirements.txt;

linting:
	pylint -E app/

tests:
	. venv/bin/activate; \
	python manage.py test

run:
	. venv/bin/activate; \
	python manage.py run

all: clean install linting tests run
