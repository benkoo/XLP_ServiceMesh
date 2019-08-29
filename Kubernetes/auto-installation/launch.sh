#!/bin/sh
# 在本地启动Kubernetes的master节点
# 因为虚拟机网卡问题，默认的IP不一定是本机的外网可访问的IP地址，因此最好手动指定
local_ip="127.0.0.1"
kubeadm init --apiserver-advertise-address=${local_ip} --pod-network-cidr=10.244.0.0/16 --kubernetes-version=v1.15.0
export KUBECONFIG=/etc/kubernetes/admin.conf
sleep 10s
kubectl apply -f kube-flannel.yml
sleep 20s
kubectl get pods -n kube-system
