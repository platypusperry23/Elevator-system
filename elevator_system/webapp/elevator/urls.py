from django.urls import path, re_path

from webapp.elevator.api.elevator_detail import DestinationAPI, DirectionAPI, StateUpdateAPI, DoorStatusAPI, \
    DestinationFloorAPI, AssignElevatorAPI
from webapp.elevator.api.initialize import InitializationAPI
from webapp.elevator.api.user_requests import AllElevatorRequests

app_name = 'elevator_service'

urlpatterns = [
    path(r'init/', InitializationAPI.as_view(), name='initialize_api'),
    re_path(r'^(?P<elevator_id>\d+)/destination/$', DestinationAPI.as_view(), name='destination_api'),
    re_path(r'^(?P<elevator_id>\d+)/direction/$', DirectionAPI.as_view(), name='destination_api'),
    re_path(r'^(?P<elevator_id>\d+)/state/$', StateUpdateAPI.as_view(), name='state_update_api'),
    re_path(r'^(?P<elevator_id>\d+)/requests/$', AllElevatorRequests.as_view(), name='all_elevator_request'),
    re_path(r'^(?P<elevator_id>\d+)/door-status/$', DoorStatusAPI.as_view(), name='door_status_api'),
    re_path(r'^add/destination/$', DestinationFloorAPI.as_view(), name='destination_floor_api'),
    re_path(r'^get/elevator/(?P<current_floor>\d+)/$', AssignElevatorAPI.as_view(), name='get_elevator'),
]
