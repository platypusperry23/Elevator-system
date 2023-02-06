import logging

import coreapi
from django.db.models import F
from django.db.models.functions import Abs
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from webapp.base.decorators import validate_request
from webapp.base.exceptions import InvalidRequestException
from webapp.base.serializers import StateUpdateSerializer, DoorStatusSerializer, DestinationRequestSerializer
from webapp.base.views import ElevatorAPIView
from webapp.elevator.models import Elevator, UserRequests
from webapp.elevator.service import ElevatorService

logger = logging.getLogger(__name__)
elevator_service = ElevatorService


class DestinationAPI(ElevatorAPIView):

    def get(self, request, elevator_id: int):
        """
        Get api that tells in which direction the elevator is moving
        """
        # TODO: Add redis use-case also

        destination = Elevator.objects.filter(elevator_id=elevator_id).values('destination_floor', 'is_moving').first()

        if destination['destination_floor'] and destination['is_moving']:
            response = {
                "Floor": destination['destination_floor'],
                "Message": f"Elevator {elevator_id}' is heading to {destination['destination_floor']} floor"
            }
        elif destination['destination_floor']:
            response = {
                "Floor": destination['destination_floor'],
                "Message": f"Elevator {elevator_id}' last headed to {destination['destination_floor']} floor"
            }

        else:
            response = {
                "Message": f'No destination floor found for elevator {elevator_id} Pls check id'
            }
        return Response(data=response, status=200)


class DirectionAPI(ElevatorAPIView):
    """
    An api which tells in which direction the lift is moving.
    And since we are assuming that floors are reached instantly so mostly this api would return lift is not moving.

    """

    def get(self, request, elevator_id: int):

        elevator = Elevator.objects.filter(elevator_id=elevator_id).values('destination_floor',
                                                                           'current_floor').first()

        current_floor = elevator['current_floor']
        destination_floor = elevator['destination_floor']

        if not destination_floor or current_floor == destination_floor:
            response = {
                'message': 'Lift is Not Moving or check elevator id'
            }
        elif current_floor < destination_floor:
            response = {"manage": 'Lift is going Up'}
        else:
            response = {"message: Lift is going down"}

        return Response(data=response, status=200)


class StateUpdateAPI(ElevatorAPIView):
    schema = AutoSchema(manual_fields=[
        coreapi.Field("state", required=True, location="form", type="string")
    ])

    def put(self, request, elevator_id: int):
        """
        This is put api which is to be used by the management to update the current state of the lift
        ACTIVE, INACTIVE , DEPRECATED, UNDER_MAINTENANCE
        :return:
        """
        try:
            serializer = StateUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                raise InvalidRequestException(serializer.errors)
            data = serializer.validated_data
            state = data['state']
            Elevator.objects.filter(elevator_id=elevator_id).update(state=state)
            return Response(data={"message": "State updated successfully"}, status=200)
        except Exception as e:
            response = {
                "message": "State Update Failed",
                "reason": str(e)
            }
            return Response(data=response, status=400)


class DoorStatusAPI(ElevatorAPIView):

    schema = AutoSchema(manual_fields=[
        coreapi.Field("status", required=True, location="form", type="string")
    ])

    def put(self, request, elevator_id: int):
        """
        A put api that updates the door status based on user request.
        Allowed values are OPEN and CLOSE.
        """

        try:
            serializer = DoorStatusSerializer(data=request.data)
            if not serializer.is_valid():
                raise InvalidRequestException(serializer.errors)
            data = serializer.validated_data
            status = data['status']
            elevator = Elevator.objects.get(elevator_id=elevator_id, state=Elevator.ACTIVE)
            elevator.door_status = status
            request_type = UserRequests.DOOR_OPEN if status == Elevator.OPEN else UserRequests.DOOR_CLOSE
            elevator_service.create_and_add_request(elevator, request_type)
            return Response(data={"message": f"Door is now {status}"}, status=200)
        except Exception as e:
            response = {
                "message": "Door Status Update Failed",
                "reason": str(e)
            }
            return Response(data=response, status=400)


class DestinationFloorAPI(ElevatorAPIView):

    schema = AutoSchema(manual_fields=[
        coreapi.Field("destination", required=True, location="form", type="array", example='14, 10, 8'),
        coreapi.Field("elevator_id", required=True, location="form", type="integer", example='12')
    ])

    @validate_request(DestinationRequestSerializer)
    def post(self, request, **kwargs):
        """
            This is a post api which is used to select the floor at which we would want to go.
            Since at a time multiple people can enter the lift so they can select multiple row.
            The api decides which direction the lift should to move
        """
        try:
            to_floors = kwargs['validated_data']['destination']
            elevator_id = kwargs['validated_data']['elevator_id']

            elevator = Elevator.objects.get(elevator_id=elevator_id, state=Elevator.ACTIVE)
            if not elevator:
                return Response(data={
                    "message": "No elevator found with this id. Kindly check again"}, status=400)
            current_floor = elevator.current_floor
            # usually the first pressed button decides the direction of the lift. we can also choose the first
            # the first input as the param that decides which side to move.
            # here i have done this but the closest_floor though.
            closest_floor = elevator_service.closest_floor(to_floors, current_floor)
            to_floors.sort()

            if closest_floor > current_floor:
                logger.info(f'Elevator {elevator_id} is going up')
                elevator.destination_floor = to_floors[0]
                # considering it reaches all the floor instantly :-)
                # TODO: add an async function that would wait for 5 seconds to before updating the current_floor so
                #  that the we can show that lift is moving for that duration.
                elevator.current_floor = to_floors[0]
            else:
                elevator.destination_floor = to_floors[-1]
                elevator.current_floor = to_floors[-1]
            elevator.is_moving = False
            elevator_service.create_and_add_request(elevator, UserRequests.CHOOSE_FLOOR, from_floor=current_floor,
                                                    to_floor=to_floors)
            return Response(data={
                "message": "All destination_floor reached",
                "current_floor": elevator.current_floor
            }, status=200)
        except Exception as e:
            return Response(data={
                "message": "Error occurred while adding destination for the elevator",
                "reason": str(e)}, status=500)


class AssignElevatorAPI(ElevatorAPIView):

    def get(self, request, current_floor: int):
        """
        This is a get API which is used to assign an elevator to a user based on which floor the user is
        the api first checks which all api's are free to take requests and then based on those it checks which one is
        the closest and assigns that one to the user. After this point the elevator is put into is_moving
        state until it has reached the destination requested by the user.
        """
        try:
            closest_elevator = Elevator.objects.filter(is_moving=False, state=Elevator.ACTIVE).order_by(
                Abs(F('current_floor') - current_floor)).first()
            if not closest_elevator:
                # TODO: add a async function that checks every second to assign the elevator
                return Response(data={
                    "message": "No available elevator kindly wait!!"
                }, status=200)
            closest_elevator.is_moving = True
            closest_elevator.destination_floor = current_floor
            # Assuming the elevator is reaches instantly
            closest_elevator.current_floor = current_floor
            elevator_service.create_and_add_request(closest_elevator, UserRequests.CALL_LIFT, from_floor=current_floor)
            return Response(data={
                "Elevator_id": closest_elevator.elevator_id,
                "message": f"Elevator assigned = {closest_elevator.elevator_id}"
            }, status=200)
        except Exception as e:
            return Response(data={
                "message": "Exception occurred while assigning elevator",
                "reason": str(e)}, status=500)
