#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Get the directory where the script is stored
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

# Define the path to the Docker Compose file
COMPOSE_FILE="${SCRIPT_DIR}/../compose.yml"

# Define a cleanup function to run on script exit or interrupt
cleanup() {
  echo "Caught Ctrl+C or script exit. Cleaning up..."
  docker compose -f "$COMPOSE_FILE" down -v
}

# Trap SIGINT (Ctrl+C), SIGTERM, and EXIT
trap cleanup SIGINT SIGTERM EXIT

# Bring everything down just in case, then start fresh
docker compose -f "$COMPOSE_FILE" down -v

# Start containers
docker compose -f "$COMPOSE_FILE" up --build --remove-orphans
