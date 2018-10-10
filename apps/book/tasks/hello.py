from celery import Task


class HelloTask(Task):
    """Hello task"""

    ignore_result = True

    def run(self, *args, **kwargs):
        """Run task"""
        self.hello()

    def hello(self):
        """Print hello"""
        print('Hello')
