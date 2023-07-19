FROM scrapinghub/scrapinghub-stack-scrapy:1.3
ENV TERM xterm
ENV SCRAPY_SETTINGS_MODULE scrapping.settings
RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN  python -m playwright install-deps && python -m playwright install chromium
COPY . /app
RUN python setup.py install
