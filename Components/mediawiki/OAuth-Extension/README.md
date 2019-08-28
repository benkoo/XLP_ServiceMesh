# Mediawiki的MW-OAuth2Client插件改进

- 在SpecialOAuth2Client.php中，加入了对json解析的修改，同时支持打印json数据以供调试
- OAuth-test.py是基于Flask框架实现的简易OAuth Client，可用于测试OAuth Server是否可用，同时可查看返回的json数据的格式