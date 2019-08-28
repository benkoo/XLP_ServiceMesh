FROM docker.elastic.co/elasticsearch/elasticsearch-oss:6.5.2

COPY es_data /es_data
COPY prepare.sh /
COPY entrypoint.sh /

USER root
RUN ["/bin/sh", "-c", "/prepare.sh"]

EXPOSE 9200 9300

WORKDIR /usr/share/elasticsearch
USER elasticsearch
CMD ["/bin/sh", "-c", "/entrypoint.sh"]
