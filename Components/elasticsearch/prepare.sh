#! /bin/sh

rm -r /usr/share/elasticsearch/plugins
cp -r /es_data/plugins /usr/share/elasticsearch/plugins
chown elasticsearch:elasticsearch /usr/share/elasticsearch/plugins
