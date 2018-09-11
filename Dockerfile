FROM python:2.7.15-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /boris

ADD . /boris/

WORKDIR /boris

RUN pip install -r requirements.pip

CMD ["sh", "-c", "gunicorn boris.wsgi -b 0.0.0.0:80 -w $BORIS_WORKERS -t 600 -n ${BORIS_INSTALLATION}-worker --capture-output --enable-stdio-inheritance --access-logfile=-"]
