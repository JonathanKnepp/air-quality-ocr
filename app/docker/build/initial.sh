#!/bin/bash

# Set Linux timezone to Eastern time
rm -rf /etc/localtime && ln -s /usr/share/zoneinfo/America/New_York /etc/localtime

# Create project directory
mkdir -p /opt/app

apt-get update || exit 1

# Install nodejs / npm
apt-get install nodejs npm -y || exit 1

# Install erlang / rabbitMQ for task queue
apt-get install -y erlang-base \
                       erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                       erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                       erlang-runtime-tools erlang-snmp erlang-ssl \
                       erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl || exit 1

# Install dependencies
apt-get update --fix-missing || exit 1
apt-get install -y locate net-tools rabbitmq-server nano sqlite3 postgresql postgresql-contrib python3-psycopg2 libpq-dev curl --allow-remove-essential --fix-missing || exit 1