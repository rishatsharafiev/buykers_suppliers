from celery import shared_task


@shared_task
def hello_periodic():
    """Hello periodic task"""
    print('Hello periodic task')
