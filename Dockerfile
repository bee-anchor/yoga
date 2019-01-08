FROM python:alpine3.8

COPY / /tmp/yoga
COPY setup.py /tmp/yoga

RUN pip install --upgrade pip && pip install /tmp/yoga && rm -r /tmp/yoga