#! /bin/sh
# 利用软链接将所有所需的数据链接到/var/www/html中
rm -rf /var/www/html/LocalSettings.php 
ln -s /wiki_data/LocalSettings.php /var/www/html/LocalSettings.php 
rm -rf /var/www/html/extensions   
ln -s /wiki_data/extensions /var/www/html/extensions  
rm -rf /var/www/html/skins    
ln -s /wiki_data/skins /var/www/html/skins    
#/bin/cp /wiki_data/logo.png /var/www/html/resources/assets/logo.png     
rm -rf /usr/local/etc/php  
ln -s /wiki_data/php /usr/local/etc/php 
ln -s /wiki_data/piwik.js /var/www/html/piwik.js    
rm -rf /var/www/html/images
ln -s /wiki_data/images /var/www/html/images 
