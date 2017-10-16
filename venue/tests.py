from django.test import TestCase, RequestFactory
from .models import Booking, Venue
from django.utils import timezone
import mock
from django.contrib.auth.models import User
from .views import approve_booking
# Create your tests here.
class CreateBooking(TestCase):
    def setUp(self):
        v = Venue.objects.create(name="Test Hall")
        print("Created Booking")
        u = User.objects.create_user('dean','tornadoalert@gmail.com','testpassword123')
        booking = Booking.objects.create(title="Some Event",venue=v,start_time=timezone.now(),end_time=timezone.now()+timezone.timedelta(hours=1))
    def test_booking(self):
        a = Booking.objects.first()
        self.assertIsNotNone(a)

class BookingModelCase(TestCase):
    def setUp(self):
        v = Venue.objects.create(name="Test Hall")
        self.user = User.objects.create_superuser('dean','tornadoalert@gmail.com','testpassword123')
        self.factory = RequestFactory()
        booking = Booking.objects.create(title="Some Event", venue=Venue.objects.get(name='Test Hall'),start_time=timezone.now(),end_time=timezone.now()+timezone.timedelta(hours=1))
    #@mock.patch('venue.models.send_email')
    #def test_send_email(self, mock_delay):
     #   pass
    
    def test_send_email(self):
        #print(u.has_perm('attendance.preclaim_dean_approve'))
        with mock.patch('venue.models.send_email.delay') as mock_email:
            booking = Booking.objects.create(title="Some Event",venue=Venue.objects.get(name='Test Hall'),start_time=timezone.now(),end_time=timezone.now()+timezone.timedelta(hours=1))
            self.assertTrue(mock_email.called)
            #mock_email.assert_called_with(to_email='tornadoalert@gmail.com')
            kwargs = mock_email.call_args[1]
            self.assertEqual(kwargs['recipient_list'],['tornadoalert@gmail.com'])
    #with mock.patch('venue.views.send_email.delay') as mock_email:

    def test_create_event(self):
        with mock.patch('venue.views.insert_event.delay') as mock_insert:
            request = self.factory.get('/')
            request.user = User.objects.get(username='dean')
            response = approve_booking(request,1)
            self.assertTrue(mock_insert.called)
