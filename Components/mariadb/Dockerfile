FROM mariadb:10.3

COPY docker-entrypoint-initdb.d /

CMD ["/bin/bash", "-c", "/docker-entrypoint.sh"]
