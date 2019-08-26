# Galera Cluster

为解决集群内数据库的高可用性需求，使用了Galera Cluster，实现了数据库集群内每一个节点均可读可写、
节点之间数据实时同步、有少数节点宕机后集群依然能正常工作的功能。

本部分参考自https://github.com/severalnines/galera-docker-mariadb，
该项目已经基于Galera实现了完善的MariaDB集群动态扩容、数据同步的功能。
仍然存在的缺陷主要是etcd集群没有动态扩容的功能，同时也无法应对etcd节点宕机的情况。
本部分在其基础上增加了etcd自动缩扩容和健康检查的部分。
