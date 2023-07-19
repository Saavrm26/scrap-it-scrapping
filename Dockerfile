FROM python:3.11.4

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

ADD . /scrap-it-scrapping/

WORKDIR /scrap-it-scrapping

EXPOSE 8080

RUN python -m venv /py && \
  /py/bin/pip install -r /tmp/requirements.txt

RUN  /py/bin/python -m playwright install-deps && /py/bin/python -m playwright install chromium


ENV PATH="/py/bin:$PATH"

CMD bash -c "python server.py"