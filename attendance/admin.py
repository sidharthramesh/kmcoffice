from django.contrib import admin
from .models import Batch, Event, PreClaim, Claim, Department, Student

# Register your models here.
admin.site.register(Batch)
admin.site.register(PreClaim)
admin.site.register(Event)
admin.site.register(Department)
admin.site.register(Student)
