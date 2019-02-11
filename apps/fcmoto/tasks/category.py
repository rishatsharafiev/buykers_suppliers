from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .page import page_task
from ..models import Category, Page
from ..parsers import CategoryParser


@shared_task(bind=True, max_retries=3)
def category_task(self, category_id):
    """Category task"""
    category = None

    try:
        category = Category.objects.get(id=category_id)

        # set status
        category.status = Category.STATUS_CHOICE_PROGRESS
        category.save()

        # parse category's pages
        category_parser = CategoryParser(category_link=category.link)
        pages = category_parser.get_pages()

        # update pages
        for page in pages:
            page, _ = Page.objects.update_or_create(page_url=page, category=category,
                                                    defaults={'status': Page.STATUS_CHOICE_NEW})
            page_task.delay(page_id=page.id)

        # set status
        category.status = Category.STATUS_CHOICE_DONE
        category.save()
    except ObjectDoesNotExist:
        pass
    except ConnectionError:
        if category and hasattr(category, 'save'):
            # set status
            category.status = Category.STATUS_CHOICE_ERROR
            category.save()

            # retry task
            self.retry(countdown=10)
