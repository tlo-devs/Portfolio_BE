FROM prom/prometheus

COPY /server/prometheus.yml /etc/prometheus/

EXPOSE 9090
