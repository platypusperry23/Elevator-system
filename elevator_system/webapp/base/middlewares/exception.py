import logging

from django import http
from django.shortcuts import render


logger = logging.getLogger(__name__)


class ExceptionMiddleWare(object):
    @staticmethod
    def process_exception(request, exception):
        logger.info("request.path " + request.path)

        # request for an html page
        if isinstance(exception, http.Http404):
            template = 'desktop/404.html'
        else:
            template = 'desktop/500.html'
        response = render(request, template)
        response.status_code = 404 if isinstance(exception, http.Http404) else 500

