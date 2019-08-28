# Mediawiki LaTeX插件

本插件支持用户在<tex></tex>标签中输入完整的LaTeX文档代码，编译并以图像形式显示在页面上的功能。
依赖后端安装的pdflatex编译环境。

## 使用方法

在Mediawiki的LocalSettings.php中添加一行

include '$IP/extensions/FreeTex/FreeTex.php';

即可