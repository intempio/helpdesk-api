import uuid
from datetime import datetime

from django.db import models
from django.utils.timezone import get_current_timezone
from model_utils.models import TimeStampedModel


class Event(TimeStampedModel):
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=50, blank=True)
    program_id = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    ac_link = models.URLField(blank=True)

    class Meta:
        ordering = ['-modified', '-created']

    # def __str__(self):
    #     return f'{self.event_name}'

    @property
    def is_today(self):
        if self.date:
            return (self.date - datetime.now(get_current_timezone())).days == 0
        return False


class Attendee(TimeStampedModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['-modified', '-created']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name}'


class EventAttendee(TimeStampedModel):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='event_attendee')
    attendee = models.ForeignKey('Attendee', on_delete=models.CASCADE, related_name='event_attendee')
    pre_registered = models.BooleanField(default=False)
    call_complete = models.BooleanField(default=False)

    @property
    def redirect_lookup_id(self):
        return str(self.pk + 123456789)

    class Meta:
        ordering = ['-modified', '-created']
