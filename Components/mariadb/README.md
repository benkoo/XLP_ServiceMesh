# MariaDB

本系统中使用的MariaDB依赖的是官方发布的Docker镜像 (见https://hub.docker.com/_/mariadb)
包含了docker-compose和Kubernetes两种发布方式，其中包括的内容有

- 镜像的指定
- 挂载路径的设置
- 常用环境变量

> 注：MariaDB与MySQL功能基本相同，将其中的镜像换成MySQL也可以使用