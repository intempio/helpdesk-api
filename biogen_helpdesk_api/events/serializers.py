from rest_framework import serializers
from.models import Event, Attendee, EventAttendee

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class EventAttendeeSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = EventAttendee
        fields = '__all__'


class AttendeeSerializer(serializers.ModelSerializer):
    event_attendee = EventAttendeeSerializer(many=True, read_only=True)

    class Meta:
        model = Attendee
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'email', 'modified',
            'created', 'event_attendee'
        )
