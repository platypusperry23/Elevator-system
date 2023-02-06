from rest_framework.status import *


class InvalidRequestException(Exception):

    def __init__(self, error):
        super(InvalidRequestException, self).__init__()
        self.message = 'Invalid Request'
        self.error = error
        self.status_code = HTTP_400_BAD_REQUEST

    def __str__(self):
        return self.message
