# pull official base image
FROM python:3.8.1-alpine

# set work directory
# WORKDIR /usr/src/app

# set environment variables...
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1


# Set working directory for the purpose of this Dockerfile
WORKDIR /home/quart

# Copy requirements to the app root
COPY ./requirements.txt ./

RUN apk add --update openssl && \
    rm -rf /var/cache/apk/*

# Create a virtual environment and install the dependecies
RUN openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout key.pem -out cert.pem -subj "/C=US/ST=VA/L=DC/O=OrgName/OU=IT Department/CN=example.com"
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev\
    && pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip


#RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Copy the app into our user root
COPY . /home/quart/

# "--keyfile", "key.pem",

CMD ["hypercorn",  "--certfile", "cert.pem", "-b", "0.0.0.0:5000", "app.main:blog_app", "--reload", "--workers", "1", "--log-level", "DEBUG"]