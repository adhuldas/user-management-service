FROM python:3.12.4

RUN useradd -m -s /bin/bash chat-user
COPY requirements.txt /src/requirements.txt
WORKDIR /src/

RUN pip install -r requirements.txt
COPY apps /src/apps
COPY constants /src/constants
COPY config.py /src/config.py
COPY run.py /src/run.py
COPY Dockerfile /src/Dockerfile
COPY Dockerfile.celery /src/Dockerfile.celery
USER chat-user
EXPOSE 5000

ENTRYPOINT [ "gunicorn","run:app","-w","1","--bind","0.0.0.0:5000", "--log-level","debug" ]
