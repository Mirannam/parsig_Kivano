from bs4 import BeautifulSoup
import requests
from pprint import pprint as pp
import csv

CSV = 'kivano.csv'
HOST = 'https://www.kivano.kg'
URL = 'https://www.kivano.kg/mobilnye-telefony'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params, verify=False)
    return response
def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='pull-right rel')
    comps = []

    for item in items:
        comps.append({
            "title": item.find('div', class_='listbox_title oh').get_text(strip=True),
            "price": item.find('div', class_='listbox_price text-center').get_text(strip=True),
            'description': item.find('div', class_='product_text pull-left').get_text(strip=True),
            "availability": item.find('div', class_='listbox_motive text-center').find('span').get_text(strip=True),
            "link": HOST + item.find('a').get('href'),
        })
    return comps


def save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Названия', 'Описание товара', 'в наличии товара', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['description'] , item['availability'], item['link']])


def pagination():
    PAGENATION = input("Введите количество страниц: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        new_list = []
        for page in range(1, PAGENATION):
            print(f"Страница №{page} готова!")
            html = get_html(URL, params={'page': page})
            new_list.extend(parse(html.text))
        save(new_list, CSV)
        print("Парсинг готов")
    else:
        print("Error")
pagination()
