from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from requests.exceptions import ConnectionError

from .product import product_task
from ..models import Page, Product
from ..parsers import PageParser


@shared_task(bind=True, max_retries=3)
def page_task(self, page_id):
    """Page task"""
    page = None

    try:
        page = Page.objects.get(pk=page_id)

        # set status
        page.status = Page.STATUS_CHOICE_PROGRESS
        page.save()

        page_parser = PageParser(page_url=page.page_url)

        # set product.is_active False
        Product.objects.filter(category=page.category, page=page).update(is_active=False)

        # save new links and update old ones
        links = page_parser.get_links()
        for link in links:
            Product.objects.update_or_create(category=page.category, link=link,
                                             defaults={
                                                 'page': page,
                                                 'status': Product.STATUS_CHOICE_NEW,
                                                 'is_active': True,
                                             })

        # get all products from page for parsing
        products = list(Product.objects.filter(category=page.category, page=page))

        recycle = True
        slice_count = 10
        product_ids = []

        while recycle:
            # collect product ids
            for i in range(slice_count):
                try:
                    product_ids.append(products.pop().pk)
                except IndexError:
                    recycle = False
                    break

            if not product_ids:
                break

            # run task
            product_task.delay(product_ids=product_ids)
            product_ids = []

        # set status
        page.status = Page.STATUS_CHOICE_DONE
        page.save()
    except ConnectionError:
        if page and hasattr(page, 'save'):
            # set status
            page.status = Page.STATUS_CHOICE_ERROR
            page.save()

            # retry task
            self.retry(countdown=10)
    except ObjectDoesNotExist:
        pass
