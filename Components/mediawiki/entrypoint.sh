#!/bin/sh
# Mediawiki的启动初始化脚本
echo Initializing...
export MW_INSTALL_PATH=/var/www/html

# 执行update.php更新数据库
php $MW_INSTALL_PATH/maintenance/update.php --quick

# CirrusSearch插件的初始化，具体步骤的说明详见CirrusSearch的README文档
sed -i --follow-symlinks "/\$wgSearchType = 'CirrusSearch';/d" $MW_INSTALL_PATH/LocalSettings.php
sed -i --follow-symlinks '$ a \$wgDisableSearchUpdate = true;' $MW_INSTALL_PATH/LocalSettings.php

php $MW_INSTALL_PATH/extensions/CirrusSearch/maintenance/updateSearchIndexConfig.php

if [ -z "$SERVER_URL" ]; then
  SERVER_URL="http:\/\/localhost"
fi
sed -i --follow-symlinks "s/SERVER_URL/${SERVER_URL}/g" $MW_INSTALL_PATH/LocalSettings.php

sed -i --follow-symlinks '/\$wgDisableSearchUpdate = true;/d' $MW_INSTALL_PATH/LocalSettings.php

php $MW_INSTALL_PATH/extensions/CirrusSearch/maintenance/forceSearchIndex.php --skipLinks --indexOnSkip
php $MW_INSTALL_PATH/extensions/CirrusSearch/maintenance/forceSearchIndex.php --skipParse

sed -i --follow-symlinks "$ a \$wgSearchType = 'CirrusSearch';" $MW_INSTALL_PATH/LocalSettings.php

# 启动Apache服务器，容器正式开始工作
apachectl -e info -D FOREGROUND
