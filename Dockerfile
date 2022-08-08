FROM ubuntu:20.04

LABEL maintainer="tomer.klein@gmail.com"


ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV API_KEY ""
ENV DB_USER ""
ENV DB_PASS ""
ENV DB_HOST ""
ENV DB_PORT 3306
ENV DB_NAME ""
ENV SLEEP_TIME 3600
ENV NOTIFIERS ""

RUN apt update -yqq

RUN apt install -yqq python3-pip && \
    apt install -yqq libffi-dev && \
    apt install -yqq libssl-dev

RUN  pip3 install --upgrade pip --no-cache-dir && \
     pip3 install --upgrade setuptools --no-cache-dir

RUN mkdir -p /opt/certi

COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

COPY certi /opt/certi

WORKDIR /opt/certi

ENTRYPOINT python3 certi.py