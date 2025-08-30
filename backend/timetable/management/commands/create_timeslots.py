from django.core.management.base import BaseCommand
from timetable.models import TimeSlot

class Command(BaseCommand):
    help = 'Creates the default time slots for the timetable'

    def handle(self, *args, **kwargs):
        # Delete existing time slots
        TimeSlot.objects.all().delete()
        
        # Create new time slots
        slots = [
            (1, '9:00 - 9:50'),
            (2, '9:50 - 10:40'),
            (3, '10:40 - 11:30'),
            (4, '11:30 - 12:20'),
            (5, '12:20 - 1:10'),
            (6, '1:10 - 2:00'),
            (7, '2:00 - 2:50'),
            (8, '2:50 - 3:40'),
            (9, '3:40 - 4:30'),
            (10, '4:30 - 5:20'),
        ]
        
        for slot_number, _ in slots:
            TimeSlot.objects.create(slot_number=slot_number)
            self.stdout.write(self.style.SUCCESS(f'Created time slot {slot_number}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully created all time slots')) 