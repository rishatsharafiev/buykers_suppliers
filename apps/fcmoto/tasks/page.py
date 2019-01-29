from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from ..models import Page, Product
from ..parsers import PageParser


@shared_task(bind=True, max_retries=3, queue='fcmoto_page')
def page_task(self, page_id):
    """Page task"""
    try:
        page = Page.objects.get(pk=page_id)
        page_parser = PageParser(page.page_url)
        links = page_parser.get_links()
        [Product.objects.get_or_create(category=page.category, link=link) for link in links]
    except ConnectionError:
        self.retry(countdown=10)
    except ObjectDoesNotExist:
        pass
