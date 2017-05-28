#!/usr/bin/env bash
docker run -e "FLASK_CONFIG=development" -p 443:443 -p 80:80 -v /var/db:/var/db -i -t flask_starter
