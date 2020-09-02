FROM nginx:stable

RUN rm /etc/nginx/nginx.conf
RUN mkdir /etc/nginx/logs

COPY ["./server/nginx.conf", "/etc/nginx/"]
