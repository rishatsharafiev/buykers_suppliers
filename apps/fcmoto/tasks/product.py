from celery import shared_task
from selenium.common.exceptions import WebDriverException

from ..models import Product
from ..parsers import ProductParser


@shared_task(bind=True, max_retries=3)
def product_task(self, product_ids):
    """Product task"""
    try:
        products = Product.objects.filter(id__in=product_ids)
        products_items = [{'id': product.id, 'link': product.link} for product in products]
        product_parser = ProductParser()
        items = product_parser.get_products(products_items=products_items)
        # items: [{'id':1 , 'price':23412, ..}, {'id':2 , 'price':2342, ..}, ..]

        for item in items:
            product, _ = Product.objects.get_or_create(id=item['id'])
            if item['status'] == Product.STATUS_CHOICE_DONE:
                product.name = item['name']
                product.manufacturer = item['manufacturer']
                product.name_url = item['name_url']
                product.price = item['price']
                product.front_picture = item['front_picture']
                product.back_picture = item['back_picture']
                product.description_text = item['description_text']
                product.description_html = item['description_html']
                product.attributes = item['attributes']

                product.status = Product.STATUS_CHOICE_DONE
                product.save()
            elif item['status'] == Product.STATUS_CHOICE_ERROR:
                product.status = Product.STATUS_CHOICE_ERROR
                product.save()

    except (ConnectionError, WebDriverException):
        self.retry(countdown=10)
