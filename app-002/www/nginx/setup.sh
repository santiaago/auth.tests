#!/bin/bash

envsubst '\$API_HOST_PORT \$API_HOST' < "/etc/$NGINX_TEMPLATE" > "/etc/nginx/conf.d/default.conf"
nginx -g 'daemon off;'