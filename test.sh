#!/bin/bash

type=$1
fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

# run server-side tests
server() {
  docker-compose -f docker-compose-dev.yml up -d --build
  docker-compose -f docker-compose-dev.yml run users python manage.py test
  inspect $? users
  docker-compose -f docker-compose-dev.yml run users flake8 project
  inspect $? users-lintba
  docker-compose -f docker-compose-dev.yml run exercises python manage.py test
  inspect $? exercises
  docker-compose -f docker-compose-dev.yml run exercises flake8 project
  inspect $? exercises-lint
  docker-compose -f docker-compose-dev.yml down
}

# run client-side tests
client() {
  docker-compose -f docker-compose-dev.yml up -d --build
  docker-compose -f docker-compose-dev.yml run client npm test -- --coverage
  inspect $? client
  docker-compose -f docker-compose-dev.yml down
}

# run e2e tests
e2e() {
  docker-compose -f docker-compose-dev.yml up -d --build
  docker-compose -f docker-compose-dev.yml run users python manage.py recreate-db
  docker-compose -f docker-compose-dev.yml run exercises python manage.py recreate-db
  docker-compose -f docker-compose-dev.yml run exercises python manage.py seed-db
  ./node_modules/.bin/cypress run --config baseUrl=http://localhost  --env REACT_APP_API_GATEWAY_URL=$REACT_APP_API_GATEWAY_URL,LOAD_BALANCER_STAGE_DNS_NAME=http://localhost
  inspect $? e2e
  docker-compose -f docker-compose-dev.yml down
}

# run all tests
all() {
  docker-compose -f docker-compose-dev.yml up -d --build
  docker-compose -f docker-compose-dev.yml run users python manage.py test
  inspect $? users
  docker-compose -f docker-compose-dev.yml run users flake8 project
  inspect $? users-lint
  docker-compose -f docker-compose-dev.yml run exercises python manage.py test
  inspect $? exercises
  docker-compose -f docker-compose-dev.yml run exercises flake8 project
  inspect $? exercises-lint
  docker-compose -f docker-compose-dev.yml run client npm test -- --coverage
  inspect $? client
  docker-compose -f docker-compose-dev.yml down
  e2e
}

# run appropriate tests
if [[ "${type}" == "server" ]]; then
  echo ""
  echo "Running server-side tests!"
  server
elif [[ "${type}" == "client" ]]; then
  echo ""
  echo "Running client-side tests!"
  client
elif [[ "${type}" == "e2e" ]]; then
  echo ""
  echo "Running e2e tests!"
  e2e
else
  echo ""
  echo "Running all tests!"
  all
fi

# return proper code
if [ -n "${fails}" ]; then
  echo ""
  echo "Tests failed: ${fails}"
  exit 1
else
  echo ""
  echo "Tests passed!"
  exit 0
fi

echo ""
