from rest_framework import serializers
from .models import Event, Attendee, EventAttendee

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class AttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendee
        fields = '__all__'

class EventAttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventAttendee
        fields = '__all__'
