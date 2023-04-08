# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime

import pymysql
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings


class MutevedioPipeline:
    def __init__(self):
        settings = get_project_settings()

        self.host = settings['HOST']
        self.port = settings['PORT']
        self.user = settings['USER']
        self.passwd = settings['PASSWD']
        self.db = settings['DB']
        self.character = settings['CHARACTER']
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.passwd,
            db=self.db,
            charset=self.character
        )
        # 创建游标
        self.cursor = self.conn.cursor()
        sql = 'use mute'
        self.cursor.execute(sql)

    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()

    def process_item(self, item, spider):
        if spider.name == 'mute':
            play_url = item['paly_url']
            cartoon_menu_id = item['cartoon_menu_id']
            episode = item['episode']
            name = item['name']
            m3u8_url = item['m3u8_url']
            sql = 'select id from player_list where m3u8_url="%s" ' % m3u8_url
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if not res:
                sql = 'insert into player_list (is_show,created_time,updated_time,episode,player_url,name,cartoon_menu_id,m3u8_url) ' \
                      'values (%d,"%s","%s","%s","%s","%s",%d,"%s")' % (
                          1, datetime.now(), datetime.now(), episode, play_url, name, cartoon_menu_id, m3u8_url)
                try:
                    self.cursor.execute(sql)
                    self.conn.commit()
                    print(f'存储{name}{episode}成功！！')
                except Exception as e:
                    print(e)
                    self.conn.rollback()
            return item


class NewmutePipeline:
    def __init__(self):
        settings = get_project_settings()

        self.host = settings['HOST']
        self.port = settings['PORT']
        self.user = settings['USER']
        self.passwd = settings['PASSWD']
        self.db = settings['DB']
        self.character = settings['CHARACTER']
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.passwd,
            db=self.db,
            charset=self.character
        )
        # 创建游标
        self.cursor = self.conn.cursor()
        sql = 'use mute'
        self.cursor.execute(sql)

    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()

    def process_item(self, item, spider):
        if spider.name == 'new_mute':
            url = item['url']
            title = item['title']
            note = item['note']
            img_url = item['img_url']
            name = item['name']
            years = item['years']
            country = item['country']
            tag = item['tag']
            introduction = item['introduction']
            sql = 'select id from cartoon_menu where title="%s"' %title
            self.cursor.execute(sql)
            exist = self.cursor.fetchone()
            if exist:
                try:

                    sql = 'update cartoon_menu set note="%s",updated_time="%s" where id = "%s"' %(note,datetime.now(),exist[0])
                    self.cursor.execute(sql)
                    self.conn.commit()
                except Exception as e:
                    self.conn.rollback()
                    print(e)
            else:
                try:
                    sql = 'insert into cartoon_menu (href,title,note,img_url,is_show,created_time,updated_time) values ("%s","%s","%s","%s",%d,"%s","%s")' % (
                        url, title, note, img_url, 1, datetime.now(), datetime.now())
                    self.cursor.execute(sql)
                    self.conn.commit()
                    sql = 'select id from cartoon_menu where title="%s"' %title
                    self.cursor.execute(sql)
                    id = self.cursor.fetchone()[0]
                    sql = 'insert into cartoon_detail (name,years,country,tag, introduction, cartoon_menu_id, is_show,created_time,updated_time)' \
                          'values ("%s","%s","%s","%s","%s",%d,%d,"%s","%s")' % (
                              name, years, country, tag, introduction, id, 1, datetime.now(), datetime.now())
                    self.cursor.execute(sql)
                    self.conn.commit()
                    sql = 'select id from cartoon_detail where name = "%s"' % title
                    self.cursor.execute(sql)
                    cartoon_detail_id = self.cursor.fetchone()[0]
                    sql = 'update cartoon_menu set cartoon_detail_id = "%d" where title = "%s"' % (cartoon_detail_id,title)
                    self.cursor.execute(sql)
                    self.conn.commit()
                except Exception as e:
                    self.conn.rollback()
                    print(e)
            print(title,'存储完成')




        return item
