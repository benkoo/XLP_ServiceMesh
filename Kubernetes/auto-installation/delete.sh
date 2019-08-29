#!/bin/sh
# 删除所有容器镜像并卸载相应的软件
rm -r /var/lib/etcd
docker rmi `docker images -q` -f
apt remove -y docker.io kubelet kubeadm kubectl 
apt autoremove -y
