#!/usr/bin/env bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

if [ ! -d /var/db ]; then
    mkdir /var/db
    cp app/flask_starter.db /var/db/flask_starter_dev.db
    cp app/flask_starter.db /var/db/flask_starter_prod.db
    chown -R www-data:www-data /var/db
fi


