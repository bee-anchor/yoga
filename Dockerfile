FROM python:alpine3.8

COPY / /tmp/faf
COPY setup.py /tmp/faf

RUN pip install --upgrade pip && pip install /tmp/faf && rm -r /tmp/faf