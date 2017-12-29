# -*- coding: utf-8 -*-
import requests
from requests.exceptions import RequestException
import re
from urllib.parse import *
import math
import pymongo

# 实例化MONGODB连接信息
client = pymongo.MongoClient('localhost')
db = client['WeChatRobot']

city = '090200'   # 成都

headers = {
  'cookie': 'search=keyword%3D%E7%88%AC%E8%99%AB%26%7C%26jobarea%3D '+city + '; m_search=areacode%3D' + city,   # 他的城市在cookies中 成都:090200 北京:010000 上海:020000
  'Host': 'm.51job.com',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}

def get_data(keyword, page=1):
  data = {   # 构建post 传输的data数据
    'keyword': keyword,
    'keywordtype': '2',
    'pageno': page,
  }
  url = 'http://m.51job.com/search/joblist.php?' + urlencode(data)
  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      response.encoding = 'utf-8'
      return response
    return None
  except RequestException:
    return None

# 匹配URL
def get_page(html):

  pattern = re.compile(r'结果约<span>(.*?)</span>', re.S)
  # 正则表达式
  item = re.search(pattern, html).group(0)   # 匹配内容

  return item[9:-7]

# 匹配URL
def get_url(html):
  pattern = re.compile(r'http:.*?search.*?jobdetail.*?obid=(.*?)&jobtype=0', re.S)
  items = re.findall(pattern, html)
  for item in items:
    yield {
      'url': 'http://m.51job.com/search/jobdetail.php?jobid=' + item + '&jobtype=0'
    }

def get_position(html):
  # print(html)
  pattern = re.compile(r'<div class="jt">.*?<p>(.*?)</p>.*?<span>(.*?)</span>.*?<em>(.*?)</em>.*?<p class="jp">(.*?)</p>.*?"s_n">(.*?)</span>.*?"s_x">(.*?)</span>.*?href="(.*?)".*?class="c_444">(.*?)</p>.*?class="at">(.*?)</div>.*?href="(.*?)" class.*?arr a2"><span>(.*?)</span></a>.*?<article>(.*?)</article>.*?welfare"><span>(.*?)</span></div>', re.S)
  items = re.findall(pattern, html)
  # print('第一次匹配', items)
  if items == []:
    pattern = re.compile(r'<div class="jt">.*?<p>(.*?)</p>.*?<span>(.*?)</span>.*?<em>(.*?)</em>.*?<p class="jp">(.*?)</p>.*?"s_n">(.*?)</span>.*?href="(.*?)".*?class="c_444">(.*?)</p>.*?class="at">(.*?)</div>.*?href="(.*?)" class.*?arr a2"><span>(.*?)</span></a>.*?<article>(.*?)</article>.*?welfare"><span>(.*?)</span></div>', re.S)
    items = re.findall(pattern, html)
    # print('第二次匹配', items)
    if items == []:
      pattern = re.compile(r'<div class="jt">.*?<p>(.*?)</p>.*?<span>(.*?)</span>.*?<em>(.*?)</em>.*?<p class="jp">(.*?)</p>.*?href="(.*?)".*?class="c_444">(.*?)</p>.*?class="at">(.*?)</div>.*?href="(.*?)" class.*?arr a2"><span>(.*?)</span></a>.*?<article>(.*?)</article>.*?welfare"><span>(.*?)</span></div>', re.S)
      items = re.findall(pattern, html)
      # print('第三次匹配', items)
      if items == []:
        pattern = re.compile(r'<div class="jt">.*?<p>(.*?)</p>.*?<span>(.*?)</span>.*?<em>(.*?)</em>.*?<p class="jp">(.*?)</p>.*?href="(.*?)".*?class="c_444">(.*?)</p>.*?class="at">(.*?)</div>.*?href="(.*?)" class.*?arr a2"><span>(.*?)</span></a>.*?<article>(.*?)</article>', re.S)
        items = re.findall(pattern, html)
        # print('第四次匹配', items)
        for item in items:
          yield {
            '职位名称': item[0],
            '时间': item[1],
            '地区': item[2],
            '工资': item[3],
            '公司信息URL': item[4],
            '公司名称': item[5],
            '公司类型': item[6],
            '公司地图URL': item[7],
            '上班地址': item[8][5:],
            '职位描述': item[9],
          }

      else:
        for item in items:
          yield {
            '职位名称': item[0],
            '时间': item[1],
            '地区': item[2],
            '工资': item[3],
            '公司信息URL': item[4],
            '公司名称': item[5],
            '公司类型': item[6],
            '公司地图URL': item[7],
            '上班地址': item[8][5:],
            '职位描述': item[9],
            '福利待遇': item[10]
          }
    else:
      for item in items:
        yield {
          '职位名称': item[0],
          '时间': item[1],
          '地区': item[2],
          '工资': item[3],
          '工作经验': item[4],
          '公司信息URL': item[5],
          '公司名称': item[6],
          '公司类型': item[7],
          '公司地图URL': item[8],
          '上班地址': item[9][5:],
          '职位描述': item[10],
          '福利待遇': item[11]
        }

  else:
    for item in items:
      yield {
        '职位名称': item[0],
        '时间': item[1],
        '地区': item[2],
        '工资': item[3],
        '工作经验': item[4],
        '学历要求': item[5],
        '公司信息URL': item[6],
        '公司名称': item[7],
        '公司类型': item[8],
        '公司地图URL:': item[9],
        '上班地址': item[10],
        '职位描述': item[11],
        '福利待遇': item[12]
      }

def save_to_mongo(data):
  if db['51job'].update({'公司名称': data['公司名称']}, {'$set': data}, True):   # 更新到MONGODB
    print('Saved to Mongodb', data['公司名称'])
    # return data   # 返回更新数据
  else:
    print('Saved to Mongodb Failed',  data['公司名称'])
  # return False

def mian():
  keyword = '爬虫'
  html = get_data(keyword).text
  page= get_page(html)
  print('共找到' + page + '个' + keyword + '职位')
  page = int(math.ceil(int(page) / 30))
  for i in range(1, page+1):
    html = get_data(keyword, i).text
    for url in get_url(html):
      # time.sleep(2)
      html = requests.get(url['url'], headers=headers)
      html.encoding = 'utf-8'
      for data in get_position(html.text):
        save_to_mongo(data)
        print('data', data)

if __name__ == '__main__':
    mian()
