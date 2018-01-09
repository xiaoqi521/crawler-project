import requests
from requests.exceptions import RequestException
import os
import re

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Host':'i.meizitu.net',
'Upgrade-Insecure-Requests':'1',
'If-None-Match': '5a3fbdf7-19b35',
'Referer': 'http://www.mzitu.com/113473',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}
# 获取网页内容
def get_page(url):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response
    return None
  except RequestException:
    return None

# 匹配图集URL
def get_url(html):
  pattern = re.compile('<br>.*?日.*?<a href="(.*?)" target="_blank">(.*?)</a>', re.S)
  # 正则表达式
  items = re.findall(pattern, html)   # 匹配内容

  for item in items:
    yield {
      'url': item[0],   # 图片URL
      'name': item[1],   # 图集名称
    }

# 匹配图片URL
def get_image_url(html):
  # print(html)
  pattern = re.compile("img\s+src=\"(.*?)\".*?dots'>…</span>.*?<span>(-?[1-9]\d*)</span></a><a.*?<span>.*?</a>", re.S)
  # 正则表达式
  items = re.findall(pattern, html)   # 匹配内容

  for item in items:
    yield {
      'img_url': item[0][:-6],
      'number': item[1]
    }

# 创建目录
def mkdir(path):
  path = path.strip()
  # 判断路径是否存在
  isExists = os.path.exists(path)
  # 判断结果
  if not isExists:
    # 如果不存在则创建目录
    # print('新建了名字叫做', path, '的文件夹')
    # 创建目录操作函数
    os.makedirs(path)
    return True
  else:
    # 如果目录存在则不创建，并提示目录已存在
    # print('名为', path, '的文件夹已经创建成功')
    return False

# 下载图片
def save_img(img, img_name, number):   # 这个函数保存图片
  path = str('/home/seven/图片/mzitu/' + img_name + '/')   # 图片保存路径
  mkdir(path)
  name = path + img_name + str(number) + '.jpg'   # 图片保存路径加图片名字
  print('正在写入图片', name)
  with open(str(name), 'wb') as f:
   f.write(img.content)   # 写入图片
   f.close()

# 主体函数
def main():
  html = get_page('http://www.mzitu.com/all/').text   # 获取图集URL
  for item in get_url(html):   # 正则表达式解析一下
    print('图集链接:' + item['url'])
    html = get_page(item['url']).text   # 获取图集页面HTML代码
    for img_number in get_image_url(html):   # 正则表达式解析图片链接
      for number in range(1, int(img_number['number']) + 1):   # 注意:这里用字符串拼接的方法获取到了图片URL少访问多次网页,但是兼容性并不是很强!
        if len(str(number)) != 2:
          number = '0' + str(number)   # 使用笨办法在10以下的数字前面加上0
        img_url = img_number['img_url'] + str(number) + '.jpg'   # 字符串拼接!
        img = requests.get(img_url, headers=headers)   # 直接get请求,但是可能会遇到错误!
        save_img(img, item['name'], number)   # 保存图片
  return True   #

# 开始运行
if __name__ == '__main__':
  if main():
    print('执行完毕')
