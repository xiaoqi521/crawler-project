#coding=utf-8
import requests
from multiprocessing import Pool
from requests.exceptions import RequestException
import re
import json

#获取页面信息
def get_one_page(url):
  try:
    headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36'
                           +' (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      return response.text
    return None
  except RequestException:
    return None

#正则表达式匹配信息
def parse_one_page(html):
  pattern = re.compile('<dd>.*?oard-index-.*?">(.*?)</i>.*?data-src="(.*?)".*?name"><a href.*?">(.*?)</a>'
                       +'.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)'
                        +'?</i></p>.*?</dd>', re.S)

  items = re.findall(pattern, html)

  for item in items:
    yield {
      'index': item[0],
      'image': item[1],
      'title': item[2],
      'actor': item[3].strip()[3:],
      'time': item[4].strip()[5:],
      'score': item[5]+item[6],
    }

#写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
      f.write(json.dumps(content, ensure_ascii=False) + '\n')
      f.close()

#爬取多页
def main(offset):
  url = 'http://maoyan.com/board/4?offset=' + str(offset)
  html = get_one_page(url)
  for item in parse_one_page(html):
    print(item)
    write_to_file(item)

#开始-----多线程
if __name__ == '__main__':
     pool = Pool()
     pool.map(main, [i*10 for i in range(10)])



