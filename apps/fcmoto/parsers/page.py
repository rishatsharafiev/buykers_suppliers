import pydash
import requests
from bs4 import BeautifulSoup


class PageParser:
    """Page parser"""

    def __init__(self, page_url):
        """Init"""
        self.page_url = page_url
        self.soup = self.get_soup()

    def get_soup(self):
        """Get soup"""
        page = requests.get(self.page_url, timeout=30)
        soup = BeautifulSoup(page.text, 'lxml')
        return soup

    def get_links(self):
        """Get products links from page"""
        item_cards = self.soup.find_all('div', class_='ListItemProductContainer ProductDetails')
        base_page_url = 'https://www.fc-moto.de/epages/fcm.sf/ru_RU/'
        links = [base_page_url + pydash.get(card, 'a.href') for card in item_cards]
        return links
