FROM nginx:1.30.0-alpine3.23-slim

RUN apk upgrade --no-cache && apk add openssl
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d/

RUN rm /var/log/nginx/access.log
RUN rm /var/log/nginx/error.log

RUN mkdir /etc/nginx/certs
RUN touch /var/log/nginx/access.log
RUN touch /var/log/nginx/error.log
RUN chown -R nginx: /etc/nginx/ /var/log/nginx/ /var/cache/nginx/
