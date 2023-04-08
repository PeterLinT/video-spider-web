# -*- coding:utf-8 -*-
import time

import requests
from lxml import etree
import json
import re
import base64
from urllib.parse import unquote
def getBYGA(url):
    url = 'http://www.freeok.vip/vodplay/13111-1-1.html'
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    res = requests.get(url,headers=header)
    player = re.search('>var player_aaaa=(.*?)<',res.text).group(1)
    jsonp = json.loads(player)
    url = jsonp['url']
    BYGA = unquote(base64.b64decode(url).decode('utf-8'))
    return BYGA

res = requests.get('https://play.freeok.vip/?url=BYGA-42ea605e5cffdef2e0fd77df13dc112b')
# print(res.text)
res = re.search('var config = (.*?);',res.text,re.S).group(1)
res = json.loads(res)
# print(res)
BYGA = res['url']
# time = res['time']
time = str(int(time.time()))
key = res['key']
url = 'https://play.freeok.vip/API.php'
data = {
    'url':BYGA,
    'time':time,
    'key':key
}

print(data)
header = {
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
res  = requests.post(url=url,data=data,headers=header)
print(res.text)