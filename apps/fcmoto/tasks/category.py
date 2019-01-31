from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .page import page_task
from ..models import Category, Page
from ..parsers import CategoryParser


@shared_task(bind=True, max_retries=3)
def category_task(self, category_id):
    """Category task"""
    try:
        category = Category.objects.get(id=category_id)
        category_parser = CategoryParser(category.link)
        pages = category_parser.get_pages()

        for page in pages:
            page, _ = Page.objects.get_or_create(page_url=page, category=category)
            page_task.delay(page_id=page.id)

    except ObjectDoesNotExist:
        pass
    except ConnectionError:
        self.retry(countdown=10)
