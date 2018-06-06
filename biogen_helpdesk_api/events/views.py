from datetime import datetime

from django.db.models import Q
from django.utils.timezone import get_current_timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Attendee, Event, EventAttendee
from .serializers import (AttendeeSerializer, EventAttendeeSerializer,
                          EventSerializer)

from rest_framework.views import APIView
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import urlencode
from django.http import HttpResponseRedirect


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
    filter_backends = (SearchFilter,)
    search_fields = ('first_name', 'last_name')

    @action(detail=False)
    def recent(self, request):
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
