import requests
import time
from multiprocessing import Pool
# 定义请求头
headers = {
	'Host': 'www.toutiao.com',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
	'Referer': 'https://wx2.qq.com/',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1',
	'Cache-Control': 'max-age=0',

}
def get_proxy():
	return requests.get("http://127.0.0.1:5010/get/").content


def delete_proxy(proxy):
	requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_Html():
	# ....
	retry_count = 5
	proxy = get_proxy()
	while retry_count > 0:
		try:
			html = requests.get('https://www.toutiao.com/i6507892465364632071/',
			                    proxies={"http": "http://{}".format(proxy)}, headers=headers)
			# 使用代理访问
			# time.sleep(3)
			return html
		except Exception:
			retry_count -= 1
	# 出错5次, 删除代理池中代理
	delete_proxy(proxy)
	return None


def main(i):
	html = get_Html()


if __name__ == '__main__':
	pool = Pool()
	pool.map(main, [i * 1 for i in range(1000)])
