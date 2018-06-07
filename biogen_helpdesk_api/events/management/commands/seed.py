from django.core.management.base import BaseCommand

from biogen_helpdesk_api.events.factories import EventAttendeeFactory, AttendeeFactory


class Command(BaseCommand):
    help = 'Seed data'

    def handle(self, *args, **options):
        self.stdout.write("Start seeding data.....")

        EventAttendeeFactory.create_batch(100)
        AttendeeFactory.create_batch(50)

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
