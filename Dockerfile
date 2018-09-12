FROM python:2.7.15-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /boris

WORKDIR /boris

ADD ./requirements.pip /boris/requirements.pip

RUN pip install -r requirements.pip

ADD ./boris /boris/boris

CMD ["sh", "-c", "gunicorn boris.wsgi -b 0.0.0.0:80 -w $BORIS_WORKERS -t 600 -n ${BORIS_INSTALLATION}-worker --access-logfile - --error-logfile - --log-level debug"]
