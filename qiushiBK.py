# -*- coding:utf-8 -*-
import requests
from requests.exceptions import RequestException
import re
import pymongo
import time

# 配置信息
MONGO_URL = 'localhost'
MONGO_DB = 'qiushiBK'
MONGO_TABLE = 'product'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_page(url):
  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      return response.text   # 返回网页源代码
    return None
  except RequestException:
    print('请求出错!')
    return None

def page_data(html):

  pattern = re.compile('"author clearfix">\n<a href="(.*?)".*?<h2>\n(.*?)\n</h2>.*?articleGender (.*?)Icon">(.*?)</div>.*?<span>\n\n\n(.*?)\n\n</span>.*?number">(.*?)</i>.*?number">(.*?)</i> 评论', re.S)
  # 正则表达式
  items = re.findall(pattern, html)   # 匹配内容

  for item in items:
    yield {
      'userurl': 'https://www.qiushibaike.com/' + item[0],   # 用户URL
      'name': item[1],   # 用户昵称
      'gender': item[2],   # 用户性别
      'age': item[3],   # 用户年龄
      'content': item[4],   # 内容
      'thumb up': item[5],   # 点赞数量
      'comment': item[6],   # 评论数量
    }

# 数据保存到MONGODB
def save_to_mongo(result):
  try:
    if db[MONGO_TABLE].insert(result):
      print('存储到MONGODB成功！', result)
  except Exception:
    print('存储到MONGODB失败！', result)



def main(offset):
  url = 'https://www.qiushibaike.com/hot/page/' + str(offset)
  html = get_page(url)
  for item in page_data(html):
    save_to_mongo(item)




if __name__ == '__main__':
  page = '300'   # 爬取页数
  for i in range(1, int(page)):
    main(i)
    time.sleep(1)   # 给服务器喘口气
    print('第' + str(i) + '页')
