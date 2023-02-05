import functools
import logging

from webapp.base.exceptions import InvalidRequestException

logger = logging.getLogger(__name__)


def validate_request(validation_serializer):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(cls, request, *args, **kwargs):
            if request.method == 'GET':
                request_data = request.query_params
            else:
                request_data = request.data
            serializer = validation_serializer(data=request_data)
            if not serializer.is_valid():
                logger.error(
                    "invalid request exception %s request data %s " %
                    (serializer.errors, request_data))
                raise InvalidRequestException(serializer.errors)
            kwargs['validated_data'] = serializer.validated_data
            kwargs['serializer'] = serializer
            return func(cls, request, *args, **kwargs)

        return wrapper

    return decorator
