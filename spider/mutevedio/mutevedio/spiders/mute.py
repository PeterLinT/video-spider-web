import re

import pymysql
import scrapy
from urllib import parse

from scrapy.http.response.html import HtmlResponse
import scrapy.utils.spider

from scrapy.utils.defer import maybe_deferred_to_future

origin_url = 'https://www.mutefun.com'


class MuteSpider(scrapy.Spider):
    name = 'mute'

    # allowed_domains = ['mutefun.com']
    # start_urls = ['http://mutefun.com/']
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
        sql = 'SELECT href from cartoon_menu WHERE updated_time > (NOW() - INTERVAL 5 HOUR)'
        self.cursor.execute(sql)
        url_list = self.cursor.fetchall()
        for url in url_list:

            print('开始解析', url[0])
            yield scrapy.Request(url=url[0], callback=self.parse)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def parse(self, response: HtmlResponse):
        name = response.xpath('//div[@class="module-info-heading"]/h1/text()').extract_first()
        sql = 'select id from cartoon_menu where title="%s"' % name
        self.cursor.execute(sql)
        cartoon_menu_id = self.cursor.fetchone()[0]
        a_list = response.xpath('//div[@class="module-play-list-content module-play-list-base"]/a')
        for a in a_list:
            episode = a.xpath('./span/text()').extract_first()
            url = a.xpath('@href').extract_first()
            play_url = parse.urljoin(origin_url, url)                   
            if '-1-' in url:
                yield scrapy.Request(url=play_url, callback=self.second_parse, meta={
                    'cartoon_menu_id': cartoon_menu_id,
                    'episode': episode,
                    'name': name
                })

    def second_parse(self, response: HtmlResponse):

        paly_url = response.url
        cartoon_menu_id = response.meta['cartoon_menu_id']
        episode = response.meta['episode']
        name = response.meta['name']

        print('开始解析', name, episode)

        src = response.xpath('//div[@class="player-box-main"]/script[1]/text()').extract_first()
        m3u8 = re.compile('"url":"(.*?)",')
        m3u8_url = m3u8.search(str(src)).group(1)
        if 'm3u8' not in m3u8_url:
            return
            # m3u8_url = 'https://www.mutefun.com/play/?url=' + m3u8_url
            #
            # yield scrapy.Request(url=m3u8_url, callback=self.thr_parse, meta={
            #     'paly_url': paly_url,
            #     'cartoon_menu_id': cartoon_menu_id,
            #     'episode': episode,
            #     'name': name,
            #     'm3u8_url': m3u8_url,
            # })
        else:
            yield {
                'paly_url': paly_url,
                'cartoon_menu_id': cartoon_menu_id,
                'episode': episode,
                'name': name,
                'm3u8_url': m3u8_url,
            }

    # def thr_parse(self, response: HtmlResponse):
    #     m3u8 = re.compile('"url":"(.*?)",')
    #     m3u8_url = m3u8.search(response.text).group(1)
    #     meta = response.meta
    #     meta['m3u8_url'] = m3u8_url
    #     paly_url = meta['paly_url']
    #     cartoon_menu_id = meta['cartoon_menu_id']
    #     episode = meta['episode']
    #     name = meta['name']
    #     print(f'正在传输管道,{name},{episode},{m3u8_url}')
    #     yield {
    #         'paly_url': paly_url,
    #         'cartoon_menu_id': cartoon_menu_id,
    #         'episode': episode,
    #         'name': name,
    #         'm3u8_url': m3u8_url,
    #     }
