#! /bin/bash
#export LC_ALL=C
#cp /etc/apt/sources.list /etc/apt/sources.list.bak
#cp ./sources.list /etc/apt/sources.list
apt-get update
apt-get install -y docker.io 
cp ./docker.service /lib/systemd/system/docker.service
systemctl daemon-reload
systemctl restart docker

apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet=1.15.0-00 kubeadm=1.15.0-00 kubectl=1.15.0-00


image=(
    kube-apiserver:v1.15.0
    kube-controller-manager:v1.15.0
    kube-scheduler:v1.15.0
    kube-proxy:v1.15.0
    pause:3.1
    etcd:3.3.10
    coredns:1.3.1
)

for imageName in ${image[@]} ; do
    docker pull k8s.gcr.io/$imageName
done
