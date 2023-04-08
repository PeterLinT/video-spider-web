# -*- coding:utf-8 -*-

# import pymysql
# db = pymysql.connect(
#             host="localhost",
#             port=3306,
#             user='root',  # 在这里输入用户名
#             password='',  # 在这里输入密码
#             charset='utf8mb4'
#         )
# cursor = db.cursor()
# sql = 'use mute'
# cursor.execute(sql)
# sql = 'select 1 from tv_video where player_url="%s" limit 1' % '''https://www.fantuanhd.com/play/id-14018-1-1.html'''
# cursor.execute(sql)
# a= cursor.fetchone()
# if a:
#     print(1)
# else:
#     print(0)

# import asyncio
#
#
# async def others():
#     print("start")
#     await asyncio.sleep(2)
#     print('end')
#     return '返回值'
#
#
# async def func():
#     print("执行协程函数内部代码")
#
#     # 遇到IO操作挂起当前协程（任务），等IO操作完成之后再继续往下执行。当前协程挂起时，事件循环可以去执行其他协程（任务）。
#     response1 = await others()
#     print("IO请求结束，结果为：", response1)
#
#     response2 = await others()
#     print("IO请求结束，结果为：", response2)
#
#
# asyncio.run(func())
import time
#
# col = 'AAA'
# cot = 1
# ret = 0
# lst = col[::-1]
# ret += (ord(lst[0])-64)
# for i in lst[1:]:
#     ret += (ord(i)-64)*26**cot
#     cot+=1
# print(ret)
print(time.time())