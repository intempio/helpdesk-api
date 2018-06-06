import factory

from .models import Attendee, Event, EventAttendee
from django.utils.timezone import get_current_timezone


class EventFactory(factory.django.DjangoModelFactory):
    event_name = factory.Sequence(lambda n: f'fake event {n}')
    event_type = factory.Sequence(lambda n: f'fake event type {n}')
    program_id = factory.Sequence(lambda n: f'fake program id {n}')
    date = factory.Faker('date_time_this_year', after_now=True, tzinfo=get_current_timezone())
    ac_link = 'https://intempio.adobeconnect.com/virtual_office_hours'

    class Meta:
        model = Event
        django_get_or_create = ('event_name',)


class AttendeeFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    class Meta:
        model = Attendee
        django_get_or_create = ('email',)


class EventAttendeeFactory(factory.django.DjangoModelFactory):
    pre_registered = factory.Faker('pybool')
    call_complete = factory.Faker('pybool')
    event = factory.SubFactory(EventFactory)
    attendee = factory.SubFactory(AttendeeFactory)

    class Meta:
        model = EventAttendee


class UserWithEventAttendeeFactory(EventFactory):
    event_attendee = factory.RelatedFactory(EventAttendeeFactory, 'event')
