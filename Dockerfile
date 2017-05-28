FROM ubuntu:16.04

MAINTAINER Colin Turner <koolspin245@gmail.com>

RUN apt-get update

RUN apt-get -y install \
    curl \
    vim \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt-dev \
    python3-lxml \
    libffi-dev \
    sqlite3 \
    nginx \
    supervisor

WORKDIR /root
RUN curl -O http://projects.unbit.it/downloads/uwsgi-2.0.12.tar.gz && tar xvf uwsgi-2.0.12.tar.gz
WORKDIR uwsgi-2.0.12
RUN python3 uwsgiconfig.py --build && cp ./uwsgi /usr/local/bin/

# Take advantage of Docker cached layers and only re-install when necessary
ADD requirements.txt /tmp/requirements.txt
RUN cd /tmp && pip3 install -r requirements.txt

RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/conf.d/
COPY fullchain.pem /etc/nginx/
COPY privkey.pem /etc/nginx/
RUN chown www-data:www-data /etc/nginx/privkey.pem
RUN chmod 600 /etc/nginx/privkey.pem

# The following is absolutely necessary otherwise when nginx daemonizes, supervisord will think it exited and try to restart it
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Keep this here to take advantage of cached layers
# Speeds up Docker build a lot
WORKDIR /code
ADD . /code

EXPOSE 80 443

ENV FLASK_CONFIG production
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

