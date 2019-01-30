from celery import shared_task
from selenium.common.exceptions import WebDriverException

from ..models import Product
from ..parsers import ProductParser


@shared_task(bind=True, max_retries=3)
def product_task(self, product_id=None):
    """Product task"""
    try:
        if product_id:
            ProductParser.run(product_ids=[product_id])
        else:
            products = Product.objects.all()
            ids = [product.id for product in products]
            ProductParser().run(product_ids=ids)
    except (ConnectionError, WebDriverException):
        self.retry(countdown=10)
