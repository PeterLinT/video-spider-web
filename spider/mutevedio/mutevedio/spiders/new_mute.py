import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.http.response.html import HtmlResponse
import pymysql
from urllib import parse


class NewMuteSpider(scrapy.Spider):
    name = 'new_mute'
    allowed_domains = ['mutefun.tv']
    start_urls = ['https://www.mutefun.tv/label/new.html']

    # def start_requests(self):
    #     settings = get_project_settings()
    #     self.host = settings['HOST']
    #     self.port = settings['PORT']
    #     self.user = settings['USER']
    #     self.passwd = settings['PASSWD']
    #     self.db = settings['DB']
    #     self.character = settings['CHARACTER']
    #     self.connect()
    #     yield scrapy.Request(callback=self.parse, url='https://www.mutefun.tv/label/new.html')
    #
    # def connect(self):
    #     self.conn = pymysql.connect(
    #         host=self.host,
    #         port=self.port,
    #         user=self.user,
    #         password=self.passwd,
    #         db=self.db,
    #         charset=self.character
    #     )
    #     # 创建游标
    #     self.cursor = self.conn.cursor()
    #     sql = 'use mute'
    #     self.cursor.execute(sql)
    #
    # def __del__(self):
    #     # 关闭游标
    #     self.cursor.close()
    #     # 关闭连接
    #     self.conn.close()

    def parse(self, response: HtmlResponse, **kwargs):
        a_list = response.xpath('//div[@class="module-items module-poster-items"]/a')
        count = 1
        for a in a_list:
            url = parse.urljoin(response.url, str(a.xpath('@href').extract_first()))

            title = a.xpath('@title').extract_first()

            note = a.xpath('./div[1]/div[1]/text()').extract_first()
            img_url = a.xpath('.//img/@data-original').extract_first()
            print("开始爬取", url, title, note, img_url)
            count += 1
            return
            # yield scrapy.Request(callback=self.detail_parse, url=url, dont_filter=True, meta={
            #     'url': url,
            #     'title': title,
            #     'note': note,
            #     'img_url': img_url,
            # })

    def detail_parse(self, response: HtmlResponse, **kwargs):
        url = response.meta['url']
        title = response.meta['title']
        note = response.meta['note']
        img_url = response.meta['img_url']
        name = response.xpath('//div[@class="module-info-heading"]/h1/text()').extract_first()

        years = response.xpath('//div[@class="module-info-tag-link"]/a/text()').getall()[0]
        country = response.xpath('//div[@class="module-info-tag-link"]/a/text()').getall()[1]
        tag = response.xpath('//div[@class="module-info-tag-link"]/a/text()').getall()[2:]
        try:
            introduction = response.xpath('//div[@class="module-info-introduction-content"]/p/text()').extract_first()
            introduction = str(introduction).replace('"', '')
        except:
            introduction = ''
        print(title, '进入管道')
        yield {
            'url': url,
            'title': title,
            'note': note,
            'img_url': img_url,
            'name': name,
            'years': years,
            'country': country,
            'tag': tag,
            'introduction': introduction,
        }
