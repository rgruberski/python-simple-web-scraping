import time
import requests
from slugify import slugify
from bs4 import BeautifulSoup


class PageScrapper:

    def __init__(self, url):

        self.url = url
        self.last_page = self.get_last_page_number()

        print(f"Total number of pages: {self.last_page}")

    def get_last_page_number(self):
        page = self.read_page_content(self.url)
        last_page_element = page.find("a", {"title": "ostatnia strona"})
        return int(last_page_element['data-page-number'])

    def find_advertisements(self):

        for page_number in range(self.last_page + 1):

            print(f"Page {page_number+1}/{self.last_page} processing...")

            page = self.read_page_content(self.url + f'?strona={page_number}')
            advertisements = page.findAll("a", {"class": "list__item__content__title__name link"})

            for advertisement_index in range(len(advertisements)):
                data = self.parse_advertisement(advertisements[advertisement_index]['href'])
                print(data)
                time.sleep(1)

    def parse_advertisement(self, url):

        data = {}

        page = self.read_page_content(url)
        container = page.find('div', {'class': 'section-content'})

        data['nazwa'] = container.find('h1', {'class': 'title'}).get_text().strip()
        data['tresc'] = container.find('div', {'class': 'ogl__description'}).get_text().strip()
        data['cena'] = float(container.find('span', {'class': 'oglDetailsMoney'})
                             .get_text().replace('zł', '').replace(' ', '').replace(',', '.'))

        parameters = container.findAll('div', {'class': 'oglField__container'})

        for parameter_index in range(len(parameters)):
            label = parameters[parameter_index].find('div', {'class': 'oglField__name'})
            value = parameters[parameter_index].find('span', {'class': 'oglField__value'})

            if value is not None:
                data[slugify(label.get_text())] = value.get_text()

        return data

    def read_page_content(self, url):
        page = requests.get(url)
        return BeautifulSoup(page.content, "html.parser")


URL = ''
scraper = PageScrapper(URL)
scraper.find_advertisements()
