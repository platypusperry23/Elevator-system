from rest_framework import serializers

from webapp.elevator.models import Elevator


class InitializationSerializer(serializers.Serializer):
    elevator_count = serializers.IntegerField(required=True)

    def validate(self, data):
        elevator_count = data['elevator_count']
        if elevator_count <= 0:
            raise serializers.ValidationError("Elevator Count Should be always greater than zero")
        return data


class DestinationSerializer(serializers.Serializer):
    elevator_id = serializers.IntegerField(required=True)


class StateUpdateSerializer(serializers.Serializer):
    state = serializers.CharField(required=True)

    def validate(self, data):
        valid_states = [Elevator.UNDER_MAINTENANCE, Elevator.ACTIVE, Elevator.INACTIVE, Elevator.DEPRECATED]
        state = data['state']
        if state not in valid_states:
            raise serializers.ValidationError(f'State should only have these values {valid_states}')
        return data


class DoorStatusSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)

    def validate(self, data):
        valid_status = [Elevator.OPEN, Elevator.CLOSED]
        status = data['status']

        if status not in valid_status:
            raise serializers.ValidationError(f'Status should be {valid_status} only')
        return data


class UserRequestResponseSerializer(serializers.Serializer):
    request_id = serializers.IntegerField(required=True)
    request_type = serializers.CharField(required=True)
    from_floor = serializers.IntegerField(required=False, allow_null=True)
    to_floor = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class DestinationRequestSerializer(serializers.Serializer):
    destination = serializers.ListSerializer(child=serializers.IntegerField(), required=True,
                                             max_length=20, min_length=1)
    elevator_id = serializers.IntegerField(required=True)
