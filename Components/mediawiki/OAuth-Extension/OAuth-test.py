from flask import *
from furl import furl
import jsonify
import requests
import json
import random
import string


app = Flask(__name__)

# 与OAuth Server有关的参数
client_id = '9fc354ccddfcc1214c7e'
client_secret = 'b8d5cd9dfbd131b5a9ab8b3b6b8930d611a68149'
# OAuth Server的API路径
# 示例中使用的是Github
authorize_url = 'https://github.com/login/oauth/authorize'
access_token_url = 'https://github.com/login/oauth/access_token'
access_user_url = 'https://api.github.com/user'
# 本地地址的配置，可以用域名也可以用IP
local_host = '127.0.0.1'
local_port = 5000
# 路由的配置
# 示例中的路由与Mediawiki的配置一致
callback_route = '/index.php/Special:Oauth2Client/callback'

# 其他参数，是自动生成的
# 本地URL
local_url = 'http://%s:%d' % (local_host, local_port)
# 回调URL
callback_url = local_url + callback_route
# 生成的随机字符串，防止csrf攻击
state_string = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(20,40)))


def authorize_request():
    url = authorize_url
    params = {
        'client_id': client_id,
        'redirect_url': callback_url,
        'scope': 'read:user',
        'state': state_string,
        'allow_signup': 'true'
    }
    url = furl(url).set(params)
    return redirect(url, 302)


@app.route('/', methods=['GET', 'POST'])
def index():
    return authorize_request()
    
    
@app.route('/index.php', methods=['GET', 'POST'])
def index():
    return authorize_request()


@app.route(callback_url, methods=['GET', 'POST'])
def callback():
    print('Received request:')
    print(request)
    code = request.args.get('code')
    print('Received code = ', code)
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'state': state_string
    }
    r = requests.post(access_token_url, json=payload, headers={'Accept': 'application/json'})
    access_token = json.loads(r.text).get('access_token')
    print('Received access_token = ', access_token)
    r = requests.get(access_user_url, headers={'Authorization': 'token ' + access_token})
    print(r)
    print('==========')
    print(r.text)
    return_json = json.loads(r.text)
    return return_json


if __name__ == '__main__':
    app.run('0.0.0.0', port=local_port, debug=True)
