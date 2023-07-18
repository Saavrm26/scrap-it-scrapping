FROM python:3.11.4

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

COPY ./* /scrap-it-scrapping/

WORKDIR /scrap-it-scrapping

RUN python -m venv /py && \
  /py/bin/pip install -r /tmp/requirements.txt

RUN  /py/bin/python -m playwright install chromium

RUN  rm -rf /tmp && \
  adduser \
  --disabled-password \
  --no-create-home \
  scrapy-user

ENV PATH="/py/bin:$PATH"

USER scrapy-user
