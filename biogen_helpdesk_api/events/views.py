from rest_framework import viewsets

from .models import Attendee, Event, EventAttendee
from .serializers import (AttendeeSerializer, EventAttendeeSerializer,
                          EventSerializer)


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AttendeeViewSet(viewsets.ModelViewSet):

    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer


class EventAttendeeViewSet(viewsets.ModelViewSet):

    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer
