from rest_framework import serializers

from .models import Event, Attendee, EventAttendee


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'event_name', 'event_type', 'program_id',
                  'date', 'is_today', 'ac_link', 'modified', 'created')


class EventAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendee
        fields = ('id', 'attendee', 'pre_registered', 'call_complete',
                  'modified', 'created', 'redirect_lookup_id')


class EventAttendeeReadOnlySerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = EventAttendee
        fields = ('id', 'attendee', 'pre_registered', 'call_complete',
                  'modified', 'created', 'event')


class AttendeeSerializer(serializers.ModelSerializer):
    event_attendee = EventAttendeeReadOnlySerializer(many=True, read_only=True)

    class Meta:
        model = Attendee
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'email', 'modified',
            'created', 'event_attendee',
        )
