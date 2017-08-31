from django import forms
from .models import Department, Batch, Event
from datetime import datetime, timedelta
class StudentForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    roll_no = forms.IntegerField()
    serial = forms.IntegerField()
    event = forms.ModelChoiceField(Event.objects.filter(created_at__gte=datetime.utcnow()-timedelta(days=120)),None)

class PeriodForm(forms.Form):
    name = forms.CharField(max_length=200)
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    department = forms.ModelChoiceField(Department.objects.all(),None)
    batch = forms.ModelChoiceField(Batch.objects.filter(active=True),None)