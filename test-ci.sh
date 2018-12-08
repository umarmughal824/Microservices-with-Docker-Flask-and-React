#!/bin/bash

env=$1
fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

tempInspect() {
  if [ $1 -ne 0 ]; then
    echo "error: $2"
  fi
}

# run client and server-side tests
dev() {
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
}

# run e2e tests
# new
e2e() {
  echo "Create containers"
  docker-compose -f docker-compose-$1.yml up -d --build
  tempInspect $? buildContainers
  echo "Recreate users-db"
  docker-compose -f docker-compose-$1.yml run users python manage.py recreate-db
  tempInspect $? recreateUserDB
  echo "Recreate exercises-db"
  docker-compose -f docker-compose-$1.yml run exercises python manage.py recreate-db
  tempInspect $? recreateExercisesDB
  echo "Set exercises-db"
  docker-compose -f docker-compose-$1.yml run exercises python manage.py seed-db
  tempInspect $? setExercisesDB
  echo "Running cypress test"
  ./node_modules/.bin/cypress run --config baseUrl=http://localhost --env REACT_APP_API_GATEWAY_URL=$REACT_APP_API_GATEWAY_URL,LOAD_BALANCER_STAGE_DNS_NAME=$LOAD_BALANCER_STAGE_DNS_NAME
  inspect $? e2e
  docker-compose -f docker-compose-$1.yml down
}

# run appropriate tests
if [[ "${env}" == "development" ]]; then
  echo "Running client and server-side tests!"
  dev
elif [[ "${env}" == "staging" ]]; then
  echo "Running e2e tests!"
  e2e stage
elif [[ "${env}" == "production" ]]; then
  echo "Running e2e tests!"
  e2e prod
fi

# return proper code
if [ -n "${fails}" ]; then
  echo "Tests failed: ${fails}"
  exit 1
else
  echo "Tests passed!"
  exit 0
fi
