# MariaDB

本系统中使用的MariaDB依赖的是官方发布的Docker镜像 (见https://hub.docker.com/_/mariadb)
包含了docker-compose和Kubernetes两种发布方式，其中包括的内容有

- 镜像的指定
- 挂载路径的设置
- 常用环境变量

> 注：MariaDB与MySQL功能基本相同，将其中的镜像换成MySQL也可以使用

# 预置内容的数据库

官方的mariadb镜像在初始化时会自动导入/docker-entrypoint-initdb.d目录中所有支持的数据文件
使用本目录中的Dockerfile创建的镜像会自动导入./docker-entrypoint-initdb.d目录下的数据文件，
因此将需要预置的数据库内容放进./docker-entrypoint-initdb.d目录即可