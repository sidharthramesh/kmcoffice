from django.forms import ModelForm, ValidationError
from django.forms import DateTimeInput, CharField, PasswordInput
from .models import Booking
from django.contrib.auth.forms import AuthenticationForm
from attendance.models import Batch
from .models import EventCalander
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
        venue = cleaned_data.get('venue')
        # Check all calandars in database and eventCal for the venue and time
        batches = Batch.objects.all()
        eventcals = EventCalander.objects.all()
        calids = []
        for batch in batches:
            calids.append(batch.calander_id)
        for eventcal in eventcals:
            calids.append(eventcal.calander_id)
        
        for cal in calids:
            events = service.events().list(
                calendarId=cal,
                singleEvents=True,
                timeMin=start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                timeMax=end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                ).execute()["items"]
            print(events)
            if len(events) > 0:
                for event in events:
                    if event["location"] == venue.name:
                        raise ValidationError("{} not available at requested time because of {}".format(venue.name,event["summary"]))
        return cleaned_data

class StatusForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['status']

class LoginForm(AuthenticationForm):
    username = CharField(max_length=30)
    password = CharField(max_length=30, 
                               widget=PasswordInput(attrs={'name': 'password'}))