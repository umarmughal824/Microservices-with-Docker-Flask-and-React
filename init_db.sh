#!/bin/bash

# create
docker-compose -f docker-compose-dev.yml exec exercises python manage.py recreate-db
docker-compose -f docker-compose-dev.yml exec users python manage.py recreate-db
docker-compose -f docker-compose-dev.yml exec scores python manage.py recreate-db
# seed
docker-compose -f docker-compose-dev.yml exec exercises python manage.py seed-db
docker-compose -f docker-compose-dev.yml exec users python manage.py seed-db
docker-compose -f docker-compose-dev.yml exec scores python manage.py seed-db
