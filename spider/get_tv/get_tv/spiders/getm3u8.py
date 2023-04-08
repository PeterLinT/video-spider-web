import json
import time

from asgiref.sync import sync_to_async

from fantuan.models import tv_play, tv_video, movie_play
import pymysql
import scrapy
from scrapy.http.response.html import HtmlResponse
from Crypto.Cipher import AES
import base64
from ..items import Getm3u8Item, moviem3u8Item, GetTvItem


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


class Getm3u8Spider(scrapy.Spider):
    name = 'getm3u8'

    def start_requests(self):
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user='root',  # 在这里输入用户名
            password='',  # 在这里输入密码
            charset='utf8mb4'
        )
        self.cursor = self.db.cursor()
        sql = 'use mute'
        self.cursor.execute(sql)
        # sql = 'select detail_url,id from movie_play WHERE updated_time > (NOW() - INTERVAL 5 HOUR)'
        sql = 'select detail_url,id from tv_play WHERE updated_time > (NOW() - INTERVAL 5 HOUR)'
        self.cursor.execute(sql)
        url_list = self.cursor.fetchall()

        for url, id in url_list:
            # tvplay = tv_play.objects.filter(id=id) # 拿到tvplay的对象
            # print(url,id)
            # try:
            #     movieplay = movie_play.objects.filter(id=id) # 拿到tvplay的对
            # except Exception as e:
            #     print('djangoorm错误：',e)
            print('开始解析', url)
            yield scrapy.Request(url=url, callback=self.parse, meta={'id': id})

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def parse(self, response: HtmlResponse, **kwargs):
        id = response.meta['id']
        # tvplay = response.meta['tvplay']
        # movieplay = response.meta['movieplay']
        title = response.xpath('//div[@class="stui-content__detail"]/h1/text()').extract_first()
        api_from = response.xpath('//div[@class="stui-vodlist__head"]/h3/text()').extract()
        if '融兴线路' in api_from:
            api_from.remove('融兴线路')
        if '芒果高清' in api_from:
            api_from.remove('芒果高清')
        if '自营蓝光' in api_from:
            api_from.remove('自营蓝光')

        # play_list_count= response.xpath('//ul[@class="stui-content__playlist clearfix"]').__len__()
        for i in range(len(api_from)):
            play_list = response.xpath('//ul[@class="stui-content__playlist clearfix"][{}]/li'.format(i + 1))
            for li in play_list:
                Episode = li.xpath('./a/text()').extract_first()
                player_url = response.urljoin(li.xpath('./a/@href').extract_first())
                sql = 'select 1 from movie_video where player_url="%s" limit 1' % player_url
                self.cursor.execute(sql)
                exist = self.cursor.fetchone()
                if not exist:

                    apifrom = api_from[i]
                    # video_url = get_video(player_url)
                    # time.sleep(5)
                    print(title, Episode, player_url, apifrom)
                    # items = moviem3u8Item()
                    items = Getm3u8Item()
                    items['title'] = title
                    items['api_from'] = apifrom
                    items['episode'] = Episode
                    items['player_url'] = player_url
                    # items['video_url'] = ''
                    # items['movie_play'] = id
                    items['tv_play'] = id

                    yield items

                    print(items['title'], items['episode'], '传输管道')
                else:
                    print('已存在')

