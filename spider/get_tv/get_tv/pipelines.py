from asgiref.sync import sync_to_async

from fantuan.models import movie_play
from fantuan.models import tv_play


class GetTvPipeline:
    @sync_to_async
    def process_item(self, item, spider):

        if spider.name == 'getm3u8':
            try:
                # id = item['movie_play']
                # movieplay = movie_play.objects.filter(id=id).first()  # 拿到tvplay的对
                # item['movie_play'] = movieplay

                id = item['tv_play']
                tvplay = tv_play.objects.filter(id=id).first()  # 拿到tvplay的对
                item['tv_play'] = tvplay

                # player_url = item['player_url']
                # video_url = get_video(player_url)
                # item['video_url'] = video_url



                item.save()

            except Exception as e:
                print(e)
            finally:
                print(item['title'],'存储成功')
        return item

    # @sync_to_async
    # def process_item(self, item, spider):
    #     if spider.name == 'fantuanhd':
    #         try:
    #             item.save()
    #         except Exception as e:
    #             print(e)
    #         finally:
    #             print(item['title'], '存储成功')
    #     return item


