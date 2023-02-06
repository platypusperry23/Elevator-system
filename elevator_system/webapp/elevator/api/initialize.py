import coreapi

from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from webapp.base.decorators import validate_request
from webapp.base.exceptions import InvalidRequestException
from webapp.base.serializers import InitializationSerializer
from webapp.base.views import ElevatorAPIView
from webapp.elevator.models import Elevator


class InitializationAPI(ElevatorAPIView):

    schema = AutoSchema(manual_fields=[
        coreapi.Field(name="elevator_count", required=True, location="form", type="integer", example=10)
    ])

    @validate_request(InitializationSerializer)
    def post(self, request, *args, **kwargs):
        """
        API takes number of elevators as an inputs and creates that many elevators and if there are earlier elevators
        then they are deleted.
        """
        validated_data = kwargs['validated_data']
        elevator_count = validated_data['elevator_count']
        Elevator.objects.all().delete()
        elevators = [Elevator()] * int(elevator_count)
        Elevator.objects.bulk_create(elevators)

        response = {
            'Message': f'Created {elevator_count} elevators',
        }
        response = Response(data=response, status=200)
        return response
