FROM python:3.12.3-alpine

RUN apk add bash wget curl gcc musl-dev zlib-dev
RUN wget https://github.com/margaretbloom/nash-f/releases/download/v0.0.0/httpd2 -O /usr/bin/httpd2
RUN chmod 555 /usr/bin/httpd2
COPY start.sh /usr/bin/start.sh
RUN chmod 555 /usr/bin/start.sh

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["bash", "/usr/bin/start.sh"]
