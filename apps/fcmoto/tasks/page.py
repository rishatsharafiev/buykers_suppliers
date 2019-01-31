from math import ceil

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .product import product_task
from ..models import Page, Product
from ..parsers import PageParser


@shared_task(bind=True, max_retries=3)
def page_task(self, page_id):
    """Page task"""
    try:
        page = Page.objects.get(pk=page_id)
        page_parser = PageParser(page.page_url)
        links = page_parser.get_links()

        product_ids = []
        products_per_task = 20
        for link in links:
            product, _ = Product.objects.get_or_create(category=page.category, link=link)
            product_ids.append(product.id)

        for pos in range(int(ceil(len(product_ids) / products_per_task))):
            group_ids = product_ids[pos * products_per_task:pos * products_per_task + products_per_task]
            product_task.delay(product_ids=group_ids)
    except ConnectionError:
        self.retry(countdown=10)
    except ObjectDoesNotExist:
        pass
