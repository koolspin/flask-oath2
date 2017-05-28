#!/usr/bin/env bash
# Make sure you manually remove the line below and change the secret_key env
exit 1
docker run -p 443:443 -p 80:80 -v /var/db:/var/db -e 'SECRET_KEY=XXX' -d flask_starter
