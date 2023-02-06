from rest_framework import serializers
from rest_framework.response import Response

from webapp.base.serializers import UserRequestResponseSerializer
from webapp.base.views import ElevatorAPIView
from webapp.elevator.models import Elevator, UserRequests


class AllElevatorRequests(ElevatorAPIView):

    def get(self, request, elevator_id: int):
        """
        A GET request api that returns all the request which has been received by the elevator
        """
        try:
            elevator = Elevator.objects.filter(elevator_id=elevator_id).values('user_requests').first()
            if not elevator['user_requests']:
                return Response(data={"message": "No data found kindly check elevator_id"}, status=200)

            request_ids = elevator['user_requests'].split(',')
            user_requests = UserRequests.objects.filter(request_id__in=request_ids).values('request_id',
                                                                                           'request_type',
                                                                                           'from_floor', 'to_floor')
            requests = []
            for user_request in user_requests:
                serializer = UserRequestResponseSerializer(data=user_request)
                if serializer.is_valid():
                    requests.append(serializer.data)
                else:
                    raise serializers.ValidationError(serializer.errors)
            response = {
                elevator_id: requests
            }
            return Response(data=response, status=200)
        except Exception as e:
            response = {
                "message": "Exception occurred while fetching user_requests",
                "reason": str(e)
            }
            return Response(data=response, status=500)
