FROM nginxinc/nginx-unprivileged:alpine

USER root

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

RUN mkdir /etc/nginx/certs/
COPY certs/dummy-django-restframework.crt /etc/nginx/certs/
COPY certs/dummy-django-restframework.key /etc/nginx/certs/
RUN chmod 0600 /etc/nginx/certs/dummy-django-restframework.key
RUN chown -R nginx: /etc/nginx/

USER nginx
