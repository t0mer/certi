FROM techblog/fastapi:latest

LABEL maintainer="tomer.klein@gmail.com"


ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV API_KEY ""
ENV LOG_LEVEL "DEBUG"
ENV DB_NAME ""
ENV SLEEP_TIME 7200
ENV NOTIFIERS ""

RUN apt update -yqq

RUN apt install -yqq python3-pip && \
    apt install -yqq libffi-dev && \
    apt install -yqq libssl-dev

RUN  pip3 install --upgrade pip --no-cache-dir && \
     pip3 install --upgrade setuptools --no-cache-dir && \
     pip3 install --upgrade psycopg2-binary  --no-cache-dir

RUN mkdir -p /opt/certi

COPY certi /opt/certi

WORKDIR /opt/certi

ENTRYPOINT python3 certi.py