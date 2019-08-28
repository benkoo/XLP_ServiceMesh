FROM mediawiki:1.33

COPY wiki_data /wiki_data
COPY prepare.sh /

RUN /prepare.sh

EXPOSE 80

COPY entrypoint.sh /
CMD /entrypoint.sh
