from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from ..models import Category, Page
from ..parsers import CategoryParser


@shared_task(bind=True, max_retries=3, queue='fcmoto_category')
def category_task(self, category_id):
    """Category task"""
    try:
        category = Category.objects.get(pk=category_id)
        category_parser = CategoryParser(category.link)
        soup = category_parser.get_soup()
        pages = category_parser.get_pages(soup)
        for page in pages:
            Page.objects.get_or_create(page_url=page, category=category)
    except ObjectDoesNotExist:
        pass
    except ConnectionError:
        self.retry(countdown=10)
