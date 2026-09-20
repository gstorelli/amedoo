#!/bin/sh
# Primo avvio / aggiornamento del sito sul VPS.
#   sh deploy/avvia.sh
set -e

cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Creato .env: controlla PROXY_NETWORK, ADMIN_HOST e imposta ADMIN_PASSWORD, poi rilancia."
  exit 1
fi

if [ ! -f contenuti.json ]; then
  cp contenuti.esempio.json contenuti.json
  echo "Creato contenuti.json dai testi attuali."
fi

docker compose up -d --build
docker compose ps
