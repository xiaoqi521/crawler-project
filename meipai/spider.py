from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
import json
from bs4 import BeautifulSoup
import re
from config import *
import pymongo
import os
from hashlib import md5
from multiprocessing import Pool


client =pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# 先爬取索引页
def get_page_index(offset,keyword):
  data = {
    'offset': offset,
    'format': 'json',
    'keyword': keyword,
    'autoload': 'true',
    'count': '20',
    'cur_tab': 1
  }

  url = 'https://www.toutiao.com/search_content/?'+urlencode(data)  # 把数据给格式化传入URL里面
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.text
    return None
  except RequestException:
    print('请求索引页出错！')
    return None

# 取出详情页
def parse_page_index(html):
  data = json.loads(html)              # 把数据变成json格式
  if data and 'data' in data.keys():   # 判断是否含有data
    for item in data.get('data'):      # 取出data
      yield item.get('article_url')    # 取出article_url


# 请求详情页
def get_page_data(url):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.text
    return None
  except RequestException:
    print('请求详情页出错')
    return None

# 解析详情页
def parse_page_data(html,url):
   soup = BeautifulSoup(html, 'lxml')
   title = soup.select('title')[0].get_text()
   images_pattern = re.compile('http://.*?(.*?)&quot', re.S)    # 正则表达式取出字符串
   result = images_pattern.findall(html)
   if result:
     for i in range(len(result)):              # 遍历列表拼接每个链接
       imgurl = 'http://' + result[i]

       download_image(imgurl)
     return {
       'title': title,
       'url': url,
       'imgurl': imgurl
     }

def save_to_mongo(result):
  if db[MONGO_TABLE].insert(result):
    print('存储到MongoDB成功')
    return True
  return False


def download_image(url):
  print('正在下载', url)

  try:
    response = requests.get(url)
    if response.status_code == 200:
      save_image(response.content)
    return None
  except RequestException:
    print('请求图片出错')
    return None

def save_image(content):
  file_path = '{0}/{1}.{2}'.format(os.getcwd()+'/images', md5(content).hexdigest(), 'jpg')
  if not os.path.exists(file_path):
    with open(file_path, 'wb') as f:
      f.write(content)
      f.close()



def main(offset):
  html = get_page_index(offset, KEYWORD)
  for url in parse_page_index(html):   # 取出所有详情页URL
    html = get_page_data(url)
    if html:                           # 如果HTML成功返回就调用解析详情页
      result = parse_page_data(html, url)
      print(result)
      if result:
        save_to_mongo(result)


if __name__ == '__main__':
    groups = [x*20for x in range(GROUP_START, GROUP_END+1)]
    pool = Pool()
    pool.map(main, groups)
