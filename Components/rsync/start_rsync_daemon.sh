#!/bin/bash

cp rsyncd.conf /etc/rsyncd.conf
chmod 600 password_daemon.txt
rsync --daemon --config=/etc/rsyncd.conf
