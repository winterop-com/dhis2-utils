#!/usr/bin/env bash
set -euo pipefail

rm -rf home/logs/*

docker compose down -v
docker compose build --no-cache
docker compose up --remove-orphans
