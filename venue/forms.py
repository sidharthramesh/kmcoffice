from django.forms import ModelForm, ValidationError
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
    def clean(self):
        cleaned_data = super(VenueBookingForm, self).clean()
        venue = cleaned_data.get('venue')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        # Check all calandars in database and eventCal for the venue and time
        
        if False:
            raise ValidationError("{} not available at {}".format(venue.name,start_time))
        return cleaned_data
class StatusForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['status']

class LoginForm(AuthenticationForm):
    username = CharField(max_length=30)
    password = CharField(max_length=30, 
                               widget=PasswordInput(attrs={'name': 'password'}))