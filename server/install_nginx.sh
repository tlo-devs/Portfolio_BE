#!/bin/bash

function download_nginx {
  wget http://nginx.org/download/nginx-1.18.0.tar.gz
  tar -zxvf nginx-1.18.0.tar.gz
  ls -la
}

apt-cache show wget
if [ "$?" -eq "0" ]; then
  download_nginx
else
  apt-get install wget
  download_nginx
fi

apt-get install libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev build-essential

cd nginx-1.18.0
./configure --sbin-path=/usr/bin/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --with-pcre --pid-path=/var/run/nginx.pid \
    --with-http_ssl_module

make
make install
mv ./nginx.service /lib/systemd/system/nginx.service
rm /etc/nginx/nginx.conf
mv ./nginx.conf /etc/nginx/nginx.conf
mv ./uwsgi_params /etc/nginx/uwsgi_params

systemctl start nginx
systemctl enable nginx
