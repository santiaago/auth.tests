FROM alpine:latest

RUN apk --no-cache --update-cache add python python-dev py-pip build-base

ADD ./web-api/src ./server

WORKDIR /server

RUN pip install --no-cache-dir -q -r requirements.txt

EXPOSE 80

ENV FLASK_APP=/server/server.py

CMD gunicorn -b 0.0.0.0:80 \
    --forwarded-allow-ips=* \
    --log-file - \
    --log-level debug \
    server:app