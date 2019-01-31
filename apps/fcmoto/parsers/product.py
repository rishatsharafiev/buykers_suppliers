import logging
import time
from decimal import Decimal, DecimalException

from conf import settings
from furl import furl
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..models import Product


class ProductParser:
    """Product parser"""

    logger = logging.getLogger(__name__)

    def get_element_by_css_selector(self, driver, selector):
        """Get element by CSS selector"""
        try:
            element = driver.find_element_by_css_selector(selector)
        except (NoSuchElementException, TimeoutException):
            element = None
        return element

    def get_elements_by_css_selector(self, driver, selector):
        """Get elements by CSS selector"""
        try:
            elements = driver.find_elements_by_css_selector(selector)
        except (NoSuchElementException, TimeoutException):
            elements = []
        return elements

    def get_products(self, products_items):
        """Get products"""
        capabilities = {
            "browserName": "chrome",
            "version": "70.0",
            "screenResolution": "1024x600x16",
            "enableVNC": True,
            "enableVideo": False,
            "chromeOptions": {
                'args': [
                    '--disable-notifications',
                    '--disable-logging',
                    '--disable-infobars',
                    '--disable-extensions',
                    '--disable-web-security',
                    '--no-sandbox',
                    # '--headless',
                    '--silent',
                    '--disable-popup-blocking',
                    '--incognito',
                    '--lang=ru',
                    '--ignore-certificate-errors'
                ]
            }
        }

        driver = webdriver.Remote(
            command_executor=settings.SELENOID_HUB,
            desired_capabilities=capabilities)
        # Product item: {'id': 2, 'link': 'http://link_to_item.com/'}
        products_ = []
        for product_item in products_items:
            try:
                driver.get(product_item['link'])
                new_item_data = self.get_product(driver, product_item['link'])

                new_item_data['status'] = Product.STATUS_CHOICE_DONE
                products_.append({**new_item_data, **product_item})
            except WebDriverException:
                new_item_data = None
                new_item_data['status'] = Product.STATUS_CHOICE_ERROR
                products_.append({**new_item_data, **product_item})
            finally:
                try:
                    driver.quit()
                except (WebDriverException, TimeoutException):
                    pass
        return products_

    def get_product(self, driver, link) -> dict:
        """Get single product"""
        initial_wait = WebDriverWait(driver, 3 * 60)
        initial_wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ContentAreaWrapper'))
        )

        # 'Наименование',
        name = self.get_element_by_css_selector(driver, '.ICProductVariationArea [itemprop="name"]')
        name = name.text if name else ''

        # 'Производитель',
        manufacturer = \
            self.get_element_by_css_selector(driver, '.ICProductVariationArea [itemprop="manufacturer"]')
        manufacturer = manufacturer.text if manufacturer else ''

        # 'Цвет'
        color = self.get_element_by_css_selector(driver, '.ICVariationSelect .Headline.image .Bold.Value')
        color = color.text if color else ''

        # 'Все размеры',
        all_size = self.get_elements_by_css_selector(driver, '.ICVariationSelect li > button')
        all_size = set([size.text for size in all_size] if all_size else [])

        # 'Неактивные размеры',
        disabled_size = self.get_elements_by_css_selector(driver, '.ICVariationSelect li.disabled > button')
        disabled_size = set([size.text for size in disabled_size] if disabled_size else [])

        # 'Активные размеры',
        active_size = all_size.difference(disabled_size)

        # 'Атрибуты'
        sizes = [{'available': False, 'size': size} for size in disabled_size]
        sizes.extend([{'available': True, 'size': size} for size in active_size])
        attributes = {'sizes': sizes, 'color': color}

        # 'Цена',
        price = self.get_element_by_css_selector(driver, '.PriceArea .Price')
        price = price.text if price else ''
        try:
            price_cleaned = Decimal(price.replace('руб.', '').replace(' ', '').replace(',', '.'))
        except DecimalException:
            raise DecimalException

        # 'Фотография'
        front_picture = self.get_element_by_css_selector(driver, '#ICImageMediumLarge')
        front_picture = front_picture.get_attribute('src') if front_picture else ''

        activate_second_picture = \
            self.get_element_by_css_selector(driver, '#ProductThumbBar > li:nth-child(2) > img')

        if activate_second_picture:
            activate_second_picture.click()
            time.sleep(2)
            back_picture = self.get_element_by_css_selector(driver, '#ICImageMediumLarge')
        back_picture = back_picture.get_attribute('src') if activate_second_picture and back_picture else ''

        # 'Описание'
        description = self.get_element_by_css_selector(driver, '.description[itemprop="description"]')
        description_text = description.text if description else ''
        description_html = description.get_attribute('innerHTML') if description else ''

        # 'Название url'
        f = furl(link.replace('?', ''))
        name_url = f.path.segments[-1]

        product_item = {
            'name': name,
            'manufacturer': manufacturer,
            'name_url': name_url,
            'price': price_cleaned,
            'front_picture': front_picture,
            'back_picture': back_picture,
            'description_text': description_text,
            'description_html': description_html,
            'attributes': attributes
        }
        return product_item
