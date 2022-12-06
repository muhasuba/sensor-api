.ONESHELL:

.PHONY: clean install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	virtualenv -p python3.8 venv; \
	. venv/bin/activate; \
	pip install -r requirements.txt;

dbinit:
	. venv/bin/activate; \
	python manage.py db init;  \
	python manage.py db migrate --message 'initial database migration';  \
	python manage.py db upgrade;

linting:
	pylint -E app/

tests:
	. venv/bin/activate; \
	python manage.py test

run:
	. venv/bin/activate; \
	python manage.py run

allfirst: clean install linting dbinit tests run

all: clean install tests run
