# -*- coding: utf-8 -*-
import json
import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import math
import pymongo

# 实例化MONGODB连接信息
client = pymongo.MongoClient('localhost')
db = client['zhaoping']['baidu']

# 定义请求头
headers = {
	'Host': 'zhaopin.baidu.com',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
}

# 获取网页数据这里预先定义了query='python', city = '成都', pn=0
def get_html(query='python', city = '成都', pn=0):
	# 定义城市职位关键字
	data = {
		'query': query,
		'sort_type': '1',
		'city': city,
		'detailmode': 'close',
		'rn': '100',
		'pn': pn
	}
	# 构造URL链接并编码
	try:
		url = 'http://zhaopin.baidu.com/api/quanzhiasync?' + urlencode(data)
		response = requests.get(url=url, headers=headers)
		if response.status_code == 200:
			return response
		response.cookies
		return None
	except RequestException:
		print('请求失败!')
		return None
# 解析数据
def gat_data(html):
	datas = json.loads(html)['data']['main']['data']['disp_data']   # 转换成json格式然后取出数据
	for data in datas:
		yield data   # 生成器返回

# 储存到MONGODB数据库
def save_to_mongo(data,query):
	if db[query].update({'md5_str': data['md5_str']}, {'$set': data}, True):   # 更新到MONGODB
		print('Saved to Mongodb', data['officialname'])
	# return data # 返回更新数据
	else:
		print('Saved to Mongodb Failed', data['officialname'])
	# return False

# 主函数
def main():
	try:
		query = 'Python'  # 定义要查询的职位
		city = '成都'  # 定义要查询的城市
		html = get_html(query, city, ).text  # 先获取一次取出数量
		dispNum = json.loads(html)['data']['main']['data']['dispNum']  # 转换成json格式然后取出数据
		print('一共找到:', dispNum, '个职位')
		page = int(math.ceil(int(dispNum) / 100))  # 使用math模块向上取整取出要有多少页
		for i in range(0, page):  # 循环页数
			i = i * 100  # 页数乘以100,应为一页可以显示100条数据
			html = get_html(query, city, i).text  # 这次才获取数据
			for data in gat_data(html):  # 解析出数据
				save_to_mongo(data, query)  # 在储存到MONGODB数据库
		print('爬取完毕!!!')
	except:
		print('程序出现问题,请重试!')
# 启动
if __name__ == '__main__':
	main()
