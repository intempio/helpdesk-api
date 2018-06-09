from datetime import datetime

from django.db import models
from django.utils.timezone import get_current_timezone
from model_utils import Choices
from model_utils.models import TimeStampedModel


class Event(TimeStampedModel):
    EVENT_TYPE = Choices('EOD', 'Webcast')
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(choices=EVENT_TYPE, blank=True, max_length=20)
    program_id = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    ac_link = models.URLField(blank=True)

    class Meta:
        ordering = ['date', '-modified', '-created']

    def __str__(self):
        return f'{self.event_name} - ({self.program_id}) ({self.pk})'

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

    @property
    def __str__(self):
        return f'{self.full_name} ({self.pk})'


class EventAttendee(TimeStampedModel):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='event_attendee')
    attendee = models.ForeignKey('Attendee', on_delete=models.CASCADE, related_name='event_attendee')
    pre_registered = models.BooleanField(default=False)
    call_complete = models.BooleanField(default=False)

    @property
    def redirect_lookup_id(self):
        return str(self.pk + 123456789)

    def __str__(self):
        return f'{self.pk} - {self.event} {self.attendee}'

    class Meta:
        ordering = ['-modified', '-created']
