from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

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

    queryset = EventAttendee.objects.all().select_related('attendee', 'event')
    serializer_class = EventAttendeeSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, )
    filter_fields = (
        'attendee__first_name', 'attendee__last_name', 'attendee__email',
        'event__event_name', 'event__event_type', 'event__program_id'
    )
    search_fields = ('attendee__first_name', 'attendee__last_name', 'attendee__email')
