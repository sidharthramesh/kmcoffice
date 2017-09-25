from django.contrib import admin
from .models import Booking,Venue,EventCalander
# Register your models here.
admin.site.register(Venue)
admin.site.register(EventCalander)