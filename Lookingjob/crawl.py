# coding: utf-8
import pymongo
import csv


def get_data(db):
	# 实例化MONGODB连接信息
	client = pymongo.MongoClient('localhost')
	DB = client['zhaoping'][db]
	if db == 'baidu':
		datas = DB['Python'].find()
		for data in datas:
			if 'companyaddress' in str(data) and len(data['companyaddress']) > 5:
				yield {
					'name': data['officialname'],
					'jobtitle': data['name'],
					'address': data['companyaddress']
				}

	elif db == '51job':
		datas = DB['Python'].find()
		for data in datas:
				yield {
					'name': data['公司名称'],
					'jobtitle': data['职位名称'],
					'address': data['上班地址']
				}



def save_csv(data):
	with open('data.csv', 'a', newline = "") as csvout:
		# 创建writer对象，指定文件与分隔符
		writer = csv.writer(csvout, delimiter=',')
		name = data['name']
		jobtitle = data['jobtitle']
		address = data['address']
		writer.writerows([[name,address,jobtitle]])




def main():
	for db in ['baidu','51job']:
		for data in get_data(db):
			print(data['name'],data['address'], data['jobtitle'])
			save_csv(data)



if __name__ == '__main__':
	main()
