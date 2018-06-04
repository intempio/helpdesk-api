from datetime import datetime

from django.db.models import Q
from django.utils.timezone import get_current_timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .models import Attendee, Event, EventAttendee
from .serializers import (AttendeeSerializer, EventAttendeeSerializer,
                          EventSerializer)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all().prefetch_related(
        'event_attendee__event'
    ).order_by(
        'event_attendee__event__date'
    )
    serializer_class = AttendeeSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('first_name', 'last_name')

    @action(detail=False)
    def recent_attendees(self, request):
        today = datetime.now(get_current_timezone())

        recent_attendees = self.filter_queryset(self.get_queryset())
        recent_attendees = recent_attendees.filter(
            Q(event_attendee__event__date__gte=today) | Q(event_attendee__isnull=True)
        )

        page = self.paginate_queryset(recent_attendees)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_attendees, many=True)
        return Response(serializer.data)


class EventAttendeeViewSet(viewsets.ModelViewSet):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer
