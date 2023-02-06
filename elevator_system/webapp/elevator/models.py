from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.contrib.postgres.fields import ArrayField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", auto_now=True)

    class Meta:
        abstract = True


class DefaultPermissions(models.Model):
    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'read')


class Elevator(TimeStampedModel):
    UNDER_MAINTENANCE = 'UNDER_MAINTENANCE'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    DEPRECATED = 'DEPRECATED'
    STATE_CHOICES = (
        (UNDER_MAINTENANCE, UNDER_MAINTENANCE),
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
        (DEPRECATED, DEPRECATED)
    )
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    DOOR_STATUS_CHOICE = (
        (OPEN, OPEN),
        (CLOSED, CLOSED)
    )

    elevator_id = models.AutoField(verbose_name='elevator_id', serialize=False, auto_created=True, primary_key=True)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default=ACTIVE)
    current_floor = models.PositiveIntegerField(null=True, default=0)
    destination_floor = models.PositiveIntegerField(null=True)
    door_status = models.CharField(max_length=10, choices=DOOR_STATUS_CHOICE, default=CLOSED)
    user_requests = models.CharField(max_length=10000, null=True, validators=[validate_comma_separated_integer_list])
    is_moving = models.BooleanField(null=True, default=False)

    class Meta(DefaultPermissions.Meta):
        db_table = 'elevator_details'
        verbose_name = 'elevator'
        verbose_name_plural = 'elevators'


class UserRequests(TimeStampedModel):

    DOOR_OPEN = 'open_door'
    DOOR_CLOSE = 'close_door'
    CALL_LIFT = 'call_lift'
    CHOOSE_FLOOR = 'choose_floor'
    STOP = 'stop'
    REQUEST_TYPES = (
        (DOOR_OPEN, DOOR_OPEN),
        (DOOR_CLOSE, DOOR_CLOSE),
        (CHOOSE_FLOOR, CHOOSE_FLOOR),
        (CALL_LIFT, CALL_LIFT),
        (STOP, STOP)
    )

    request_id = models.AutoField(primary_key=True, auto_created=True)
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, null=True)
    request_type = models.CharField(null=True, choices=REQUEST_TYPES, default=None, max_length=50)
    from_floor = models.IntegerField(null=True)
    to_floor = models.CharField(max_length=10000, null=True, validators=[validate_comma_separated_integer_list])

    class Meta(DefaultPermissions.Meta):
        db_table = 'user_requests'
        verbose_name = 'request'
        verbose_name_plural = 'requests'
