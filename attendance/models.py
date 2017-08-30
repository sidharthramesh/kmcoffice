from django.db import models
from venue.models import Venue
# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Batch(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    calander_id = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Period(models.Model):
    batch = models.ForeignKey(Batch,models.CASCADE,'periods')
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    department = models.ForeignKey(Department,models.CASCADE,'periods')
    venue = models.ForeignKey(Venue,related_name='periods',null=True,blank=True)

    def __str__(self):
        return ' '.join([self.name, self.department.name])

class Event(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

class PreClaim(models.Model):
    event = models.ForeignKey(Event,models.CASCADE,'preclaim')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    dean_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.event + ' Preclaim'
class Student(models.Model):
    roll_no = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    serial = models.IntegerField()

    def __str__(self):
        return ' '.join([self.name,self.roll_no])

class Claim(models.Model):
    event = models.ForeignKey(Event,models.CASCADE,'claims')
    period = models.ForeignKey(Period,related_name='claims')
    js_approved = models.BooleanField(default=False)
    sis_approved = models.BooleanField(default=False)
    student = models.ForeignKey(Student,models.CASCADE,'claims')

    def __str__(self):
        return str(self.period)


