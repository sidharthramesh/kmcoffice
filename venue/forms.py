from django.forms import ModelForm
from django.forms import DateTimeInput, CharField, PasswordInput
from .models import Booking
from django.contrib.auth.forms import AuthenticationForm
class VenueBookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time','end_time','venue','title','description','notification_email']
        labels = {
            "title":"Purpose of booking",
            "description":"More details about the event"
        }
class StatusForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['status']

class LoginForm(AuthenticationForm):
    username = CharField(max_length=30)
    password = CharField(max_length=30, 
                               widget=PasswordInput(attrs={'name': 'password'}))