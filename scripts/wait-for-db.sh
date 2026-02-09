#!/bin/bash
# Attend que la base de données MySQL soit prête

set -e

host="$1"
shift
cmd="$@"

echo "En attente de la base de données sur $host..."

until mysqladmin ping -h "$host" -u root -prootpassword --silent; do
  echo "MySQL n'est pas encore prêt - attente..."
  sleep 2
done

echo "MySQL est prêt !"
exec $cmd
