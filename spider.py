import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from datetime import datetime
import json
import os
from multiprocessing import Pool

os.chdir('/root/Documents')
os.mkdir('今日头条街拍')

#发现现在街拍网站需要时间戳，于是通过datetime获取时间戳并做处理，符合网站的格式
def get_timestamp():
	now = str(datetime.timestamp(datetime.today()))
	return now.replace('.', '')[:-3]
timestamp = get_timestamp()

#cookie，user-agent一定要有，不然会无法获取html信息或者不完整
header = {
		'cookie': 'tt_webid=6684424224767067661; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16a5d0581f3527-08bdbe7284380b-e323069-1fa400-16a5d0581f4654; tt_webid=6684424224767067661; csrftoken=ab0cb50b65f304c52246d8f16d5a569f; CNZZDATA1259612802=1467525516-1556333653-https%253A%252F%252Fwww.baidu.com%252F%7C1557041054; s_v_web_id=0f434c5fc70b3216a3100cfa8dce76ab; __tasessionId=a0bo1iwwh1557043446286',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
	}
  
def get_requests(offset):
	data = {
			'aid': 24,
			'app_name': 'web_search',
			'offset': offset,
			'format': 'json',
			'keyword': '街拍',
			'autoload': 'true',
			'count': 20,
			'en_qc': 1,
			'cur_tab': 1,
			'from': 'search_tab',
			'pd': 'synthesis',
			'timestamp': timestamp
		}

	url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)

	response = requests.get(url,headers=header)
	if response.status_code == 200:
		return response.text

def get_index(text):
	data = json.loads(text)
	# print(data['data'])
	for i in data['data']:
		yield i.get('share_url')

def get_detail_index(url):
	res = requests.get(url,headers=header)
	if res.status_code == 200:
		html = res.text
	soup = BeautifulSoup(html,'lxml')
	title = soup.select('title')[0].get_text().replace(':',' ')
	print(title)
	images_pattern = re.compile('gallery: JSON.parse\("(.*)"\)', re.S)
	result = re.search(images_pattern, html)
	images = []
	if result:
		data = json.loads(result.group(1).replace('\\', ''))
		sub_images = data.get('sub_images')
		for item in sub_images:
			image_url = item['url']
			images.append(image_url)
	else:
		image = re.compile('.*articleInfo.*content:(.*?)groupId:.*', re.S)
		item = re.findall(image, res.text)
		pattern = re.compile('https?://[\S]+', re.S)
		urls = re.findall(pattern, str(item))
		for url in urls:
			image_url = url[:-6]
			images.append(image_url)
	return title,images

def save_images(title,images):
	os.chdir('/root/Documents/今日头条街拍')
  if not os.path.exists(title):
		os.mkdir(title)
	os.chdir(title)
	for image in images:
		res = requests.get(image,headers=header)
		if res.status_code == 200:
			file_name = image[7:].replace('/','') + '.jpg'
			print('downloading...' + image)
			with open(file_name,'wb') as f:
					f.write(res.content)

def main(offset):
	text = get_requests(offset)
	urls = get_index(text)
	for url in urls:
		if 'toutiao' in str(url):
			title,images = get_detail_index(url)
			save_images(title,images)

if __name__ == '__main__':
#	main()
	pool = Pool()
	groups = ([x*20 for x in range(5)])
	pool.map(main,groups)
	pool.close()
	pool.join()
	print("下载结束")
