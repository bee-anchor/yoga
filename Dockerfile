FROM python:alpine3.8

COPY / /tmp/yoga
COPY setup.py /tmp/yoga

RUN apk update && apk add --no-cache stunnel libressl

VOLUME /etc/stunnel

RUN pip install --upgrade pip && pip install /tmp/yoga && rm -r /tmp/yoga