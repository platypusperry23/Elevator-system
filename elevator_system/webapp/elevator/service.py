from webapp.elevator.models import Elevator, UserRequests


class ElevatorService:

    @staticmethod
    def create_and_add_request(elevator, request_type, from_floor=None, to_floor=None):
        current_request = elevator.user_requests
        user_request = UserRequests.objects.create(elevator_id=elevator.elevator_id, request_type=request_type,
                                                   from_floor=from_floor, to_floor=to_floor)
        if current_request:
            elevator.user_requests = current_request + ', ' + str(user_request.request_id)
        else:
            elevator.user_requests = str(user_request.request_id)
        elevator.save()

    @staticmethod
    def closest_floor(all_floors, current_floor):
        return min(all_floors, key=lambda x: abs(x - current_floor))
