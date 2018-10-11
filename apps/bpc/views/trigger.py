import logging

from django import views
from django.http import HttpResponse


class TriggerView(views.View):
    """Trigger"""

    logger = logging.getLogger(__name__)

    def get(self, request):
        """Get"""
        self.logger.debug('debug Exception')
        self.logger.info('info Exception')
        self.logger.warning('warning Exception')
        self.logger.error('error Exception')
        return HttpResponse('OK')
