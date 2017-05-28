#!/usr/bin/env bash
# The certificates to be used for the nginx ssl engine must go here
#sudo cp /etc/ssl/certs/ssl-cert-snakeoil.pem fullchain.pem
#sudo cp /etc/ssl/private/ssl-cert-snakeoil.key privkey.pem
docker build -t flask_starter .
#rm fullchain.pem
#rm privkey.pem
