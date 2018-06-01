from rest_framework import serializers
from.models import Event, Attendee, EventAttendee

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class AttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendee
        fields = '__all__'

class EventAttendeeSerializer(serializers.ModelSerializer):
    attendee = AttendeeSerializer()
    event = EventSerializer()

    class Meta:
        model = EventAttendee
        fields = '__all__'

    def create(self, validated_data):
        event_data = validated_data.pop('event')
        attendee_data = validated_data.pop('attendee')

        event = Event.objects.create(**event_data)
        attendee = Attendee.objects.create(**attendee_data)

        instance = EventAttendee.objects.create(
            event=event, attendee=attendee, **validated_data
        )

        return instance
