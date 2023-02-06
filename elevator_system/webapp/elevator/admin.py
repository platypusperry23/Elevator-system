from django.contrib import admin

from webapp.elevator.models import Elevator


@admin.register(Elevator)
class ElevatorAdmin(admin.ModelAdmin):
    list_display = (
        'elevator_id',
        'state',
        'current_floor',
        'destination_floor',
        'door_status',
    )
    list_filter = (
        'state',
        'current_floor',
        'destination_floor',
        'door_status'
    )
    list_per_page = 50
