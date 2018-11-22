from celery import shared_task

from ..parsers import TaskParser


@shared_task
def task_parser(obj):
    """Task parser task"""
    TaskParser().run(obj)
