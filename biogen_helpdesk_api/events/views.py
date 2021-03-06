from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.http import urlencode
from django.utils.timezone import get_current_timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Attendee, Event, EventAttendee
from .serializers import (AttendeeSerializer, EventAttendeeSerializer,
                          EventSerializer)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer

    def get_queryset(self):
        today = datetime.now(get_current_timezone())
        return super().get_queryset().filter(date__gte=today)


class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all().prefetch_related(
        'event_attendee__event'
    ).order_by(
        'event_attendee__event__date'
    )
    serializer_class = AttendeeSerializer

    @action(detail=False)
    def recent(self, request):
        today = datetime.now(get_current_timezone())
        recent_attendees = self.get_queryset().filter(
            Q(event_attendee__event__date__gte=today) | Q(event_attendee__isnull=True)
        )

        page = self.paginate_queryset(recent_attendees)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_attendees, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def no_events(self, request):
        no_events_attendees = self.get_queryset().filter(event_attendee__isnull=True)

        page = self.paginate_queryset(no_events_attendees)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(no_events_attendees, many=True)
        return Response(serializer.data)


class EventAttendeeViewSet(viewsets.ModelViewSet):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer


class EventLookRedirectView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, event_id, format=None):
        look_up = int(event_id) - 123456789
        obj = get_object_or_404(EventAttendee, pk=look_up)
        params = urlencode({'guestName': f'{obj.attendee.first_name} {obj.attendee.last_name}'})
        return HttpResponseRedirect(f'{obj.event.ac_link}/?{params}')


class UpTimeView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, format=None):
        return Response('Ok')
