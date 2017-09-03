from django import forms
from .models import Department, Batch, Event
from django.utils import timezone, dateparse

class StudentForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    roll_no = forms.IntegerField()
    serial = forms.IntegerField()
    event = forms.ModelChoiceField(Event.objects.filter(created_at__gte=timezone.now()-timezone.timedelta(days=120)),None)

class PeriodForm(forms.Form):
    name = forms.CharField(max_length=200)
    start = forms.CharField(max_length=200)
    end = forms.CharField(max_length=200)
    department = forms.ModelChoiceField(Department.objects.all(),None)
    batch = forms.ModelChoiceField(Batch.objects.filter(active=True),None)

    def clean_start(self):
        data = self.cleaned_data['start']
        try:
            time = dateparse.parse_datetime(data)
            return time
        except:
            raise forms.ValidationError("Cannot parse date")
    def clean_end(self):
        data = self.cleaned_data['end']
        try:
            time = dateparse.parse_datetime(data)
            return time
        except:
            raise forms.ValidationError("Cannot parse date")

class ConfirmForm(forms.Form):
    reason = forms.CharField(required=False,widget=forms.Textarea())

class StatusForm(forms.Form):
    roll_no = forms.IntegerField()