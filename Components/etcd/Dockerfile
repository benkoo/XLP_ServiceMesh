FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install -y curl wget vim python ca-certificates openssl tar python-pip && \
    pip install flask requests && \
    wget https://github.com/etcd-io/etcd/releases/download/v3.3.10/etcd-v3.3.10-linux-amd64.tar.gz && \
    tar -zxvf etcd-v3.3.10-linux-amd64.tar.gz && \
    mv etcd-v3.3.10-linux-amd64/etc* /bin/ && \
    rm -rf etcd-v3.3.10-linux-amd64* && \
    mkdir /data
VOLUME /data
EXPOSE 2379 2380 4001 7001
ADD run.sh /bin/run.sh
ADD entrypoint.sh /bin/entrypoint.sh
ADD start_cluster.py /bin/start_cluster.py
#CMD ["/bin/bash", "-c", "entrypoint.sh"]
