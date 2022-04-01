
import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36', 'accept': '*/*'}
FILE = 'comments.csv'
ART = 'article.csv'
URL = 'https://vc.ru/new' 

def get_html(url, params=None):
	r = requests.get(url, headers=HEADERS, params=params)
	return r
# комментарии
def get_content(html,cs):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='comments__item__space')
	comments2 = []
	for item in items:
		del_commetn = item.find('span', class_='user_name')
		child_commett = item.find('a', class_='comments__item__replied_to t-link')
		if child_commett:
				comments2.append({
				'answer':item.find('a', class_='comments__item__replied_to t-link').get('data-id'),
				'svoy_id':item.find('a', class_='comments__item__date t-link').get('data-id'),
				'name': item.find('span', class_='user_name').get_text(),
				'text': item.find('div', class_='comments__item__text').get_text(),
				'data': item.find('time', class_='time').get('title'),
				'urlk': cs,
				})
		elif del_commetn:
			comments2.append({
				'answer':item.find('a', class_='comments__item__date t-link').get('data-id'),
				'svoy_id':item.find('a', class_='comments__item__date t-link').get('data-id'),
				'name': item.find('span', class_='user_name').get_text(),
				'text': item.find('div', class_='comments__item__text').get_text(),
				'data': item.find('time', class_='time').get('title'),
				'urlk': cs,
			})

	return(comments2)

# создание файла (БД)
def save_file(items, path):
	with open(path, 'w', newline='', encoding='utf-8') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['Ссылка на сайт: '])
		writer.writerow([URL])
		writer.writerow(['Имя пользователя', 'Комментарий', 'Время', 'id ответа родителя', 'Свой id', 'Ссылка'])
		for item in items:
			writer.writerow([item['name'], item['text'], item['data'], item['answer'], item['svoy_id'], item['urlk']])

#ссылки на статьи
def get_arcles(html):
 	soup = BeautifulSoup(html, 'html.parser')
 	items = soup.find_all('div', class_='feed__item l-island-round')
 	articl = []
 	for item in items:
 		art_ssilka = item.find('a', class_='content-feed__link')
 		if art_ssilka:
 			articl.append({
				'articale':item.find('a', class_='content-feed__link').get('href'),
				})
 	return(articl)	

#здесь ссылки на статьи на странице свежее записываем в файл csv
def save_article(items, path):
	with open(path, 'w', newline='', encoding='utf-8') as file:
		writer = csv.writer(file, delimiter=';')
		for item in items:
			writer.writerow([item['articale']])

#открываем файл на чтение
def read_articll(items, path):
	with open(path, newline='', encoding='utf-8') as file:
		reader = csv.DictReader(file,delimiter=";")
		for row in reader:
			print(row['Ссылки на статьи:'])

def parse():
	html = get_html(URL) 
	if html.status_code == 200:
		articl = get_arcles(html.text)
		save_article(articl, ART)
		print(f'Всего {len(articl)} статей')
		dlin = len(articl)
		print(dlin)
		comments = []
		with open("article.csv", "r") as file1:
			for line in file1:
				print(line.strip())
				count = line.strip()
				html2 = get_html(count)
				if html2.status_code == 200:
					#comments.extend(counting)
					comments3 = get_content(html2.text,count) 
					comments.extend(comments3)
					print(f'Всего {len(comments3)} комментариев')
		save_file(comments, FILE)
		print(f'Всего {len(comments)} комментариев')
	else: 
		print('Error')
parse()