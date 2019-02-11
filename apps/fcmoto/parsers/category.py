import pydash
import requests
from bs4 import BeautifulSoup


class CategoryParser:
    """Category parser"""

    def __init__(self, category_link):
        """Init"""
        self.category_link = category_link
        self.soup = self.get_soup()

    def get_soup(self):
        """Get soup"""
        page = requests.get(self.category_link, timeout=30)
        soup = BeautifulSoup(page.text, 'lxml')
        return soup

    def get_pages(self):
        """Get pages"""
        pages_list = []
        try:
            pages = self.soup.find('ul', class_='PagerSizeContainer').find_all('li')
            links = [pydash.get(page, 'a.href') for page in pages]
            page_link, last_page = tuple(links[-2].rsplit('=', 1))
            last_page = int(last_page)
            base_page_url = 'https://www.fc-moto.de/epages/fcm.sf/ru_RU/'
            for page in range(1, last_page + 1):
                pages_list.append(f'{base_page_url}{page_link}={page}')
        except AttributeError:
            pages_list.append(self.category_link)
        return pages_list
