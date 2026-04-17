#!/bin/bash
set -euo pipefail

wait_for_postgres() {
  echo ">>> Waiting for PostgreSQL to start..."
  until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; do
    echo "    postgres is unavailable - sleeping"
    sleep 1
  done
  echo ">>> Postgres is up and running."
}

# Check if already initialized
MARKER_FILE="/var/lib/postgresql/data/.init-complete"
if [[ -f "$MARKER_FILE" ]]; then
  echo ">>> Database already initialized. Skipping."
  exit 0
fi

# Step 1: Wait for PostgreSQL
wait_for_postgres

# Step 2: Configure replication if not already done
CONF_FILE="/var/lib/postgresql/data/postgresql.conf"
if ! grep -q "wal_level = logical" "$CONF_FILE"; then
  echo ">>> Configuring PostgreSQL for logical replication..."
  cat >>"$CONF_FILE" <<EOF
wal_level = logical
max_wal_senders = 10
max_replication_slots = 10
max_wal_size = 8GB
min_wal_size = 80MB

# Performance tuning
shared_buffers = 1GB
maintenance_work_mem = 512MB
work_mem = 64MB
effective_cache_size = 4GB

# SSD optimizations
random_page_cost = 1.1
effective_io_concurrency = 200
EOF
  echo ">>> Restarting PostgreSQL to apply replication settings..."
  pg_ctl -D /var/lib/postgresql/data -m fast -w restart || {
    echo "!!! Failed to restart PostgreSQL"
    exit 1
  }

  wait_for_postgres
else
  echo ">>> Replication already configured."
fi

# Step 3: Import the database
if [[ -f "/docker-entrypoint-initdb.d/dhis-backup.gz" ]]; then
  echo ">>> Importing database from dhis-backup.gz..."
  if ! zcat /docker-entrypoint-initdb.d/dhis-backup.gz | sed '/ALTER.*OWNER TO/d' | psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"; then
    echo "!!! Failed to import database."
    exit 1
  fi
  echo ">>> Database import complete."
else
  echo "!!! Backup archive not found: /docker-entrypoint-initdb.d/dhis-backup.gz"
  exit 1
fi

# Step 4: Reset every user's password to $DHIS2_PASSWORD and enable accounts
DHIS2_USER="${DHIS2_USER:-admin}"
DHIS2_PASSWORD="${DHIS2_PASSWORD:-district}"
echo ">>> Resetting all user passwords to '$DHIS2_PASSWORD' and enabling accounts..."
HASH=$(DHIS2_PASSWORD="$DHIS2_PASSWORD" python3 -c 'import bcrypt, os; print(bcrypt.hashpw(os.environ["DHIS2_PASSWORD"].encode(), bcrypt.gensalt(10)).decode())')
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 -v "hash=$HASH" <<'SQL'
UPDATE userinfo SET password = :'hash', disabled = false;
SQL
echo ">>> All users can now log in with $DHIS2_USER / $DHIS2_PASSWORD"

# Step 5: Create marker
touch "$MARKER_FILE"
echo ">>> Initialization complete."
