from django.test import TestCase
from .models import Booking, Venue
from django.utils import timezone
# Create your tests here.
class CreateBooking(TestCase):
    def setUp(self):
        v = Venue.objects.create(name="Test Hall")
        print("Created Booking")
        booking = Booking.objects.create(venue=v,start_time=timezone.now(),end_time=timezone.now()+timezone.timedelta(hours=1))
    def test_booking(self):
        a = Booking.objects.first()
        self.assertIsNotNone(a)
