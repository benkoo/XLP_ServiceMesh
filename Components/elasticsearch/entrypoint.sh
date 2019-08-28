#! /bin/sh

ulimit -l unlimited
chown elasticsearch:elasticsearch /usr/share/elasticsearch/plugins
chown elasticsearch:elasticsearch /usr/share/elasticsearch/data
elasticsearch-plugin remove x-pack
/bin/bash bin/elasticsearch
