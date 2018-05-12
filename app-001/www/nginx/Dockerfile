FROM nginx:1.13.10-alpine

RUN apk update && apk add bash

# uncomment for troubleshooting
# RUN apk update && apk add curl

RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 80

COPY ./app/build /www/data

COPY ./nginx/setup.sh /setup.sh

COPY ./nginx/default.conf /etc/default.conf
COPY ./nginx/test.conf /etc/test.conf