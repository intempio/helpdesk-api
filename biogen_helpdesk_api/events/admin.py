from django.contrib import admin

from .models import Attendee, Event, EventAttendee


@admin.register(EventAttendee)
class EventAttendeeAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendee', 'pre_registered', 'call_complete', 'created', 'modified')
    list_filter = ['event__date', 'created', 'modified', 'pre_registered', 'call_complete']
    search_fields = ['event__event_name', 'attendee__first_name', 'attendee__last_name']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_type', 'program_id', 'date', 'ac_link', 'created', 'modified')
    list_filter = ('date', 'modified', 'created')
    search_fields = ('event_name', 'program_id')

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'created', 'modified')
    list_filter = ('modified', 'created')
    search_fields = ('first_name', 'last_name', 'email')
