import requests
import re
import pymysql

# MySQL连接配置信息
config = {
	'host': '127.0.0.1',
	'port': 3306,   # MySQL默认端口
	'user': 'root',   # mysql默认用户名
	'password': '',   # 密码
	'db': 'BookCrossing',   # 数据库
	'charset': 'utf8mb4',
	'cursorclass': pymysql.cursors.DictCursor,
}

# 创建连接
con = pymysql.connect(**config)

# 定义请求头
headers = {
	'Host': 'e.jd.com',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
	'Referer': 'https://search-e.jd.com/searchDigitalBook?ajaxSearch=0&enc=utf-8&key=Clara%20Callan&page=1&pvid=zge893cj.4s3zwu',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1'
}

# 定义全局变量
item = ''

# 从MySQL数据库获取数据
def get_result():
	try:
		with con.cursor() as cursor:
			sql = "SELECT * FROM BookCrossing.`BX-Books`;"
			cursor.execute(sql)
			result = cursor.fetchall()
			for BX_books in result:
				yield {
					'ISBN': BX_books['ISBN'],
					'Book-Title': BX_books['Book-Title'],
					'Book-Author': BX_books['Book-Author'],
					'Year-Of-Publication': BX_books['Year-Of-Publication'],
					'Publisher': BX_books['Publisher'],
					'Image-URL-S': BX_books['Image-URL-S'],
					'Image-URL-M': BX_books['Image-URL-M'],
					'Image-URL-L': BX_books['Image-URL-L']
				}
	finally:
		con.close()

# 从京东获取数据,查看有没有此书籍
def get_html(book_name):   # 传入书名
	url = 'https://s-e.jd.com/Search?key=' + book_name + '&enc=utf-8&pvid=182f225cc60b43c7a4f84497719d1252'   # 构造URL链接
	response = requests.get(url=url)   # 请求
	if response.status_code == 200:
		return response.text   # 返回
	return None   # 请求失败返回None

# 如果有此书籍,获取它的URL链接
def get_wareid(html):
	pattern = re.compile(
		'J_goodsList.*?goods-list-ebook J-goods-list.*?gl-warp clearfix.*?data-sku="(.*?)".*?gl-item.*?gl-i-wrap', re.S)   # 构建正则表达式
	item = pattern.findall(html)   # 匹配
	return str(item)[2:-2]   # 用切片取出需要的数据再返回

# 获取它的分类信息
def get_class(html):
	pattern = re.compile(
		'所属分类.*?target=\'_blank\'>(.*?)</a>.*?target=\'_blank\'>(.*?)</a>.*?target=\'_blank\'>(.*?)</a>', re.S)   # 构建正则表达式
	items = re.findall(pattern, html)# 匹配
	for item in items:
		genre = item[0] + '>' + item[1] + '>' + item[2]   # 构建genre中间加上>符号
		yield genre   # 生成器返回


def save_to_mysql(BX_books, genre):  # 更新或插入操作
	cursor = con.cursor()
	sql = "UPDATE `BX-Books` SET  genre=%s WHERE ISBN=%s;"   # SQL语句
	con.escape(genre)   # 格式化SQL
	sta = cursor.execute(sql,[str(genre),BX_books['ISBN']])   # 执行SQL语句
	print(sta)   # 输出返回
	con.commit()   # 提交


def mian():
	for BX_books in get_result():   # 获取数据
		book_name = str(BX_books['Book-Title'])   # 获取数据中的书名
		html = get_html(book_name)   # 去京东查询此书籍
		html_wareid = get_wareid(html)   # 取出查询的数据
		if html_wareid:   # 如果有
			url = 'https://e.jd.com/' + str(html_wareid) + '.html'   # 构造书籍URL
			print(url)
			html = requests.get(url, headers=headers).text   # 根据URL获取数据
			for genre in get_class(html):   # 取出书籍类型
				save_to_mysql(BX_books, genre)   # 更新到MySQL数据库
				print(genre)   # 输出书籍类型

		else:   # 如果京东没有
			print(book_name, '没有此书籍')


if __name__ == '__main__':
	mian()
