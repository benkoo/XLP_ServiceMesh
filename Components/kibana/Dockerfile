FROM docker.elastic.co/kibana/kibana-oss:6.5.2

COPY entrypoint.sh /

EXPOSE 5601

WORKDIR /usr/share/kibana
USER kibana
CMD ["/bin/sh", "-c", "/entrypoint.sh"]
