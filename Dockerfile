FROM python:2.7.15-alpine

ENV PYTHONUNBUFFERED 1
ENV BORIS_PATH /boris
ENV PATH "/home/boris/.local/bin:${PATH}"

# Create custom user to avoid running as a root
RUN addgroup -g 1001 boris && \
    adduser -D -u 1001 -G boris boris && \
    mkdir $BORIS_PATH && \
    chown boris:boris $BORIS_PATH

WORKDIR $BORIS_PATH

ADD ./requirements.pip requirements.pip
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    py-mysqldb \
    gcc \
    libc-dev \
    libffi-dev \
    mariadb-dev \
    sudo \
    && sudo -u boris -H sh -c "pip install -r requirements.pip --user" \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && apk add --virtual .rundeps py-mysqldb \
    && apk del .build-deps

ADD ./boris $BORIS_PATH/boris
USER boris

CMD ["sh", "-c", "gunicorn boris.wsgi -b 0.0.0.0:8000 -w $BORIS_WORKERS -t ${BORIS_WORKER_TIMEOUT:-60} -n ${BORIS_INSTALLATION}-worker --access-logfile - --error-logfile - --log-level ${BORIS_LOG_LEVEL:-info}"]
