import re

from bs4 import BeautifulSoup
import requests

url = "https://shikimori.one/ongoings"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "lxml")

anim = []

for _ in soup.find_all('div', class_='block m0'):
    date = _.find('div', class_=re.compile(r'headline m10')).text

    for i in _.find_all('article'):
        if i.find('span', class_='name-ru') is not None:

            title = i.find('span', class_='name-ru').text
            series = i.find('span', class_='misc').findAll('span')[0].text
            time = i.find('span', class_='misc').findAll('span')[1].text

            # str = i.find('source').get('srcset')
            # str = str[str.find(', ') + 1:]
            # url_photo = str[:-2].strip()
            url_photo = i.find('img').get("src")

            url = i.find('a').get('href')

            slovar1 = dict(title=title, series=series, time=time, url_photo=url_photo, url=url)

        else:
            title = i.find('a', class_='title left_aligned')

            series = i.find('span', class_='misc').findAll('span')[0].text
            time = i.find('span', class_='misc').findAll('span')[1].text

            # str = i.find('source').get('srcset')
            # str = str[str.find(', ') + 1:]
            # url_photo = str[:-2].strip()
            url_photo = i.find('img').get("src")

            url = i.find('a').get('href')

            slovar1 = dict(title=title, series=series, time=time, url_photo=url_photo, url=url)
        slovar = dict(date=date, article=slovar1)
        anim.append(slovar)
