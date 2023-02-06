import logging
import datetime

from django.conf import settings
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.views import APIView

from webapp.base.renders import ElevatorServiceRender

logger = logging.getLogger(__name__)


class ElevatorAPIView(APIView):
    renderer_classes = (ElevatorServiceRender, )

    def initialize_request(self, request, *args, **kwargs):
        request = super(
            ElevatorAPIView,
            self).initialize_request(
            request,
            *
            args,
            **kwargs)
        if settings.DEBUG:
            self.renderer_classes += (BrowsableAPIRenderer,)
        return request

    def dispatch(self, request, *args, **kwargs):

        st = datetime.datetime.now()
        dispatcherResponse = super(
            ElevatorAPIView,
            self).dispatch(
            request,
            *args,
            **kwargs)
        et = datetime.datetime.now()

        logger.info("API {api} took {time} ms", extra={"api": str(self.__class__.__name__),
                                                       "time": int((et - st).total_seconds() * 1000)})
        return dispatcherResponse
