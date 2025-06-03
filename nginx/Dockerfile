FROM nginxinc/nginx-unprivileged:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

USER root
RUN chown -R nginx: /etc/nginx/

USER nginx
