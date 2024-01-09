FROM alpine:3.18
LABEL maintainer="Jyoti Verma <jyoverma@cisco.com>"

ENV PIP_IGNORE_INSTALLED 1

# install packages we need
RUN apk update && apk add --no-cache musl-dev openssl-dev gcc py3-configobj  \
    supervisor libffi-dev uwsgi-python3 uwsgi-http jq syslog-ng uwsgi-syslog \
    py3-pip python3-dev

# do the Python dependencies
ADD Pipfile Pipfile.lock /
RUN set -ex && pip install --no-cache-dir --upgrade pipenv && pipenv install --system

# copy over scripts to init
ADD scripts /
RUN chmod +x /*.sh
ADD code /app

# entrypoint
ENTRYPOINT ["/entrypoint.sh"]

WORKDIR app
CMD ["/start.sh"]
