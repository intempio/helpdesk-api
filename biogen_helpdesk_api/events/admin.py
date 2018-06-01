from django.contrib import admin

from .models import Attendee, Event, EventAttendee

admin.site.register(Event)
admin.site.register(EventAttendee)
admin.site.register(Attendee)
