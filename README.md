## SENSOR API

REST API which is capable of storing raw measurements from sensors as well as retrieve data aggregates from these sensors upon request


### Development Environment Setup

#### Run Docker Postgres
Note: make sure you have `docker` running and the port 5432 is available

```
docker-compose up
```

#### Environment Setup
Run this export script for setup environment (for development and using docker-compose Postgres)

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sensor_api
```

### Terminal commands
Note: make sure you have `python3` (we used python3.8) `pip` and `virtualenv` installed.

Initial installation: make install

To run test: make tests

To run application: make run

To run all commands at once : make all

Make sure to run the initial migration commands to update the database.
    
> python manage.py db init

> python manage.py db migrate --message 'initial database migration'

> python manage.py db upgrade

additional:

Run pylint error check during development can help to track errors

```bash
pylint -E app/
```

### Viewing the app ###
Open the following url on your browser to view swagger documentation
http://127.0.0.1:5000/


### References
This assignment fork/using sample from https://github.com/cosmic-byte/flask-restplus-boilerplate
Guide https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563

