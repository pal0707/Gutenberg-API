#!/bin/bash

# Check if an environment argument is passed, default to 'dev' if not
ENV=$1
if [ -z "$ENV" ]; then
  ENV="dev"
fi

# Set the appropriate .env file based on the environment
# Check if the 'postgres_data' directory exists
if [ -d "./postgres_data" ]; then
  echo "'postgres_data' directory exists. Skipping build..."
  BUILD_FLAG=""
else
  echo "'postgres_data' directory does not exist. Running build..."
  BUILD_FLAG="--build"
fi

# Set the appropriate .env file based on the environment
if [ "$ENV" == "prod" ] || [ "$ENV" == "production" ]; then
  echo "Starting Docker Compose with production environment..."
  ENV_FILE=".prod.env"
  # Run Docker Compose with the production environment in detached mode
  docker compose --env-file $ENV_FILE up $BUILD_FLAG
else
  echo "Starting Docker Compose with development environment..."
  ENV_FILE=".dev.env"
  # Run Docker Compose with the development environment in foreground mode
  docker compose --env-file $ENV_FILE up $BUILD_FLAG
fi
