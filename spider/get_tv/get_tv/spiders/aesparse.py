# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-
# @Author: Null119 微信公众号/网站：治廷君
# @Desc: { 饭团影视解析 }
# @Date: { 2022/9/16 }

import requests,re,json
import base64
from Crypto.Cipher import AES

class Aes:
    def __init__(self, block_size=16):
        """
        :param block_size: 填充的块大小，默认为16，有些是8
        """
        self.__block_size = block_size

        self.__modes = {
            'CBC': AES.MODE_CBC,
            'ECB': AES.MODE_ECB
        }
        self.__padding_s = {
            'pkcs7': self.__pkcs7padding,
            'pkcs5': self.__pkcs5padding,
            'zero': self.__zeropadding,
        }

    def __pkcs7padding(self, plaintext):
        """
        明文使用PKCS7填充
        :param plaintext: 明文
        """
        block_size = self.__block_size

        text_length = len(plaintext)
        bytes_length = len(plaintext.encode('utf-8'))
        len_plaintext = text_length if (bytes_length == text_length) else bytes_length
        return plaintext + chr(block_size - len_plaintext % block_size) * (block_size - len_plaintext % block_size)

    def __pkcs5padding(self, plaintext):
        """
        PKCS5Padding 的填充
        :param plaintext: 明文
        """
        block_size = self.__block_size

        text_length = len(plaintext)
        bytes_length = len(plaintext.encode('utf-8'))
        len_plaintext = text_length if (bytes_length == text_length) else bytes_length
        return plaintext + chr(block_size - len_plaintext % block_size) * (block_size - len_plaintext % block_size)

    def __zeropadding(self, plaintext):
        """
        zeropadding 的填充
        :param plaintext: 明文
        """
        block_size = self.__block_size

        text_length = len(plaintext)
        bytes_length = len(plaintext.encode('utf-8'))
        len_plaintext = text_length if (bytes_length == text_length) else bytes_length
        return plaintext + chr(0) * (block_size - len_plaintext % block_size)

    @staticmethod
    def __unpad(plaintext):
        pad_ = ord(plaintext[-1])
        return plaintext[:-pad_]

    def aes_encrypt(self, padding: str, plaintext: str, key: str, mode: str, iv=None, *args):
        """
        :param padding: 填充方式,
        :param plaintext: 明文
        :param key:
        :param mode:
        :param iv:
        :param args: 跟AES.new 的参数一样
        :return:
        """
        key = key.encode('utf-8')
        iv = iv.encode('utf-8')
        if mode == 'ECB':
            aes = AES.new(key, self.__modes[mode], *args)
        else:
            aes = AES.new(key, self.__modes[mode], iv, *args)
        content_padding = self.__padding_s[padding](plaintext)  # 处理明文, 填充方式
        encrypt_bytes = aes.encrypt(content_padding.encode('utf-8'))  # 加密
        return str(base64.b64encode(encrypt_bytes), encoding='utf-8')  # 重新编码

    def aes_decrypt(self, padding: str, ciphertext: str, key: str, mode: str, iv=None, *args):
        key = key.encode('utf-8')
        iv = iv.encode('utf-8')
        if mode == 'ECB':
            aes = AES.new(key, self.__modes[mode], *args)
        else:
            aes = AES.new(key, self.__modes[mode], iv, *args)
        ciphertext = base64.b64decode(ciphertext)
        plaintext = aes.decrypt(ciphertext).decode('utf-8')
        if padding == 'zero':
            return plaintext
        return self.__unpad(plaintext)



def get_video(url):
    resp=requests.get(url).text
    url=re.search(r'player_aaaa=(\{.*?\})<',resp).group(1)
    rjson=json.loads(url)
    nurl=rjson['url']
    id=rjson['id']
    sid=rjson['sid']
    nid=rjson['nid']
    headers = {
        'Referer': 'https://www.fantuanhd.com/'
    }
    url=f'https://dp.1010dy.cc/?url={nurl}&next=&id={id}&nid={nid}&from=uploadixigua'
    resp=requests.get(url,headers=headers).text

    urls=re.search(r'urls = "(.*?)"',resp).group(1)
    key='Of84ff0clf252cba'
    iv='c487ebl2e38a0faO'
    a = Aes(block_size=16)
    deurl = a.aes_decrypt('zero', urls, key, 'CBC', iv)
    print('视频地址：', deurl)
    return deurl



url='https://www.fantuanhd.com/play/id-5143-2-3.html'
get_video(url)