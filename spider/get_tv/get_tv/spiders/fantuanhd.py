import scrapy
from scrapy.http.response.html import HtmlResponse
from ..items import GetTvItem,GetMovieItem

class FantuanhdSpider(scrapy.Spider):
    name = 'fantuanhd'
    allowed_domains = ['fantuanhd.com']
    # start_urls = ['https://www.fantuanhd.com/show/id-21.html']
    base_url = 'https://www.fantuanhd.com/type/id-21-{}.html'
    # base_url = 'https://www.fantuanhd.com/show/id-20/page/{}.html'

    def start_requests(self):
        for page in range(1, 10):
            url = self.base_url.format(page)
            print('开始解析',url)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response: HtmlResponse, **kwargs):
        lis = response.xpath('//ul[@class="stui-vodlist clearfix"]//li')
        for li in lis:
            title = li.xpath('./div/a/@title').extract_first()
            href = li.xpath('./div/a/@href').extract_first()
            href = 'https://www.fantuanhd.com'+href
            img_url = li.xpath('./div/a/@data-original').extract_first()
            note = li.xpath('./div/a/span/text()').extract_first()
            print(title, href, img_url, note)
            yield scrapy.Request(url=href, callback=self.detail_parse, meta={
                'title': title,
                'href': href,
                'img_url': img_url,
                'note': note
            })


    def detail_parse(self, response: HtmlResponse, **kwargs):
        title = response.meta['title']
        detail_url = response.meta['href']
        img_url = response.meta['img_url']
        note = response.meta['note']

        text = response.xpath('//div[@class="stui-content__detail"]/p[1]/text()').extract_first()
        type = text.split('/')[0].split('：')[1].strip()
        region = text.split('/')[1].split('：')[1].strip()
        year = text.split('/')[2].split('：')[1].strip()
        performer = response.xpath('//div[@class="stui-content__detail"]/p[2]/text()').extract_first().split('：')[1]
        director = response.xpath('//div[@class="stui-content__detail"]/p[3]/text()').extract_first().split('：')[1]
        introduction = response.xpath(
            '//div[@class="stui-content__detail"]//span[@class="detail-content"]/text()').extract_first()
        print(title, detail_url, img_url, note, type, region, year, performer, director, introduction)

        item = GetTvItem()
        # item = GetMovieItem()
        item['title'] = title
        item['detail_url'] = detail_url
        item['img_url'] = img_url
        item['note'] = note
        item['type'] = type
        item['region'] = region
        item['year'] = year
        item['performer'] = performer
        item['director'] = director
        item['introduction'] = introduction
        print(title,'解析完成进入管道')
        yield item
