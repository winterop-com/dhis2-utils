# Use official PostGIS image as base — includes PostgreSQL + spatial extensions
# postgis/postgis publishes 17-3.5 as linux/amd64 only; pin the platform so
# buildx does not fail on arm64 hosts (Docker Desktop runs it via Rosetta).
FROM --platform=linux/amd64 postgis/postgis:17-3.5

# Update packages and install wal2json (logical decoding / CDC) and
# python3-bcrypt (used by initdb.sh to hash DHIS2 user passwords)
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-17-wal2json python3-bcrypt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
