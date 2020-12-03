# TODO
# 1. Make a request to the ebay.com and get a page
# 2. Collect data from each detail page
# 3. Collect all links to detail pages of each product
# 4. Write scraped data to a csv file

import csv
import requests
from bs4 import BeautifulSoup


def get_page(url):
	response = requests.get(url)
	
	if not response.ok:
		print('server responded:', response.status_code)
	else:
		soop = BeautifulSoup(response.text, 'lxml')

	return soop


def get_detail_data(soup):
	# title
	# Price
	# items sold

	try:
		h1 = soup.find('h1', id='itemTitle')
		if soup.find('h1', id='itemTitle').find('span'):
			h1.find('span').extract() 
		title = h1.text.strip()
	except:
		title = ''
	
	try:
		try:
			p = soup.find('span', id='prcIsum').text.strip()
			currency, price = p.split(' ')
		except:
			try:
				p = soup.find('span', id='prcIsum_bidPrice').text.strip()
				currency, price = p.split(' ')
			except:
				p = soup.find('span', id='mm-saleDscPrc').text.strip()
				currency, price = p.split(' ')
	except:
		currency = ''
		price = ''
	
	try:
		sold = soup.find('a',class_='vi-txt-underline').text.strip().split(' ')[0].replace('\xa0','')

	except:
		sold = ''

	data = {
		'title': title, 
		'price': price,
		'currency': currency,
		'total sold': sold
		}

	return data
	

def get_index_data(soup):
	try:
		links = soup.find_all('a', class_='s-item__link')
	except:
		links = []

	urls = [item.get('href') for item in links]
	
	return urls


def write_csv(data, url):
	with open('output.csv','a',encoding="utf-8") as csvfile:
		writer = csv.writer(csvfile)
		row = [data['title'], data['price'], data['currency'], data['total sold'], url]
		writer.writerow(row)
	

def main():
	url = 'https://www.ebay.com/sch/i.html?_nkw=laptop&_pgn=1'

	products = get_index_data(get_page(url))

	for link in products:
		data = get_detail_data(get_page(link))
		write_csv(data, link)


if __name__ == '__main__':
	main()


