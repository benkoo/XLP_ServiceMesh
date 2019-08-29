#!/bin/sh
# 关闭Kubernetes，删除相应的文件并重置网络，以便下一次启动
kubeadm reset
systemctl stop kubelet
systemctl stop docker
rm -rf /var/lib/cni/
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/
rm -rf /var/lib/etcd
ifconfig cni0 down
ifconfig flannel.1 down
ifconfig docker0 down
ip link delete cni0
ip link delete flannel.1
systemctl restart kubelet
systemctl restart docker
