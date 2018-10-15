FROM python:3.6-alpine

MAINTAINER Rishat Sharafiev <rishatsharafiev@ya.ru>

# create app path
RUN mkdir -p /app
WORKDIR /app

# Add a non-root user to prevent files being created with root permissions on host machine.
ARG USER=app
ARG UID=1000
ARG HOME=/app
RUN adduser -u $UID -s /bin/bash -D -h $HOME $USER

# apk install
RUN apk add --update --no-cache --virtual .build-deps \
	shadow python3-dev libc-dev libc6-compat zlib-dev libffi-dev ca-certificates

# update pip
RUN pip install pip==18.0

# install pipenv
RUN pip3 install pipenv==2018.7.1

# install apk
RUN apk add --update --no-cache postgresql-dev gcc musl-dev make libxslt-dev

# apk del
RUN apk del .build-deps && \
	rm -rf /var/cache/apk/* /root/.cache /tmp/*

# copy application code
ADD . /app
RUN chown -R app:app /app

# install packages
RUN pipenv install --deploy --system # --skip-lock

# use user
USER app

# Run celery
ENTRYPOINT celery -A conf worker -c 5 -l info -Q normal -Ofair
