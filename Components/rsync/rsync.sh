#!/bin/bash

# 与远程端rsync daemon有关的设置
SERVER_IP='127.0.0.1'
SERVER_DATA_TAG='data'
# 本地数据文件夹
LOCAL_DATA_DIRECTORY='/data/'
# 本地存储的密码文件位置
PASSWORD_FILE='./password_client.txt'

# 密码文件中的格式为 '用户名':'密码'，因此需要对其进行解析以得到用户名
SERVER_USER=$(cat ${PASSWORD_FILE} | tr ':' ' ' | awk '${print $1}')
chmod 600 ${PASSWORD_FILE}

rsync -vazu --progress --delete ${SERVER_USER}@${SERVER_IP}::${SERVER_DATA_TAG} ${LOCAL_DATA_DIRECTORY} --password-file=${PASSWORD_FILE}
