from django.db import models
from venue.models import Venue
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Batch(models.Model):
    semester = models.IntegerField()
    batch = models.CharField(max_length=2, choices=(('a','A'),('b','B')))
    active = models.BooleanField(default=True)
    calander_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.semester) + ' ' +self.batch

class Period(models.Model):
    batch = models.ForeignKey(Batch,models.CASCADE,'periods')
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    department = models.ForeignKey(Department,models.CASCADE,'periods')
    venue = models.ForeignKey(Venue,related_name='periods',null=True,blank=True)

    def __str__(self):
        return ' '.join([self.name, self.department.name])
    
    def calander_sync(self):
        pass
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    roll_no = models.IntegerField()
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    serial = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.roll_no)

class PreClaim(models.Model):
    add_roll_numbers = models.TextField()
    event = models.ForeignKey(Event,models.CASCADE,'preclaims')
    dean_approved = models.BooleanField(default=False)
    students = models.ManyToManyField(Student,'preclaims')

    def __str__(self):
        return str(self.event) + ' Preclaim'

@receiver(post_save, sender=PreClaim)
def create_claims(sender, instance, **kwargs):
    roll_nos = [line.split(' ')[0] for line in instance.add_roll_numbers.split('\n')]
    for roll in roll_nos:
        student = Student.objects.get_or_create(roll_no=int(roll))
        instance.students.add(student[0])
    
    #send mail to dean for confirmation



class Claim(models.Model):
    event = models.ForeignKey(Event,models.CASCADE,'claims')
    period = models.ForeignKey(Period,related_name='claims')
    pre_claim_approved = models.BooleanField(default=False)
    js_approved = models.BooleanField(default=False)
    sis_approved = models.BooleanField(default=False)
    student = models.ForeignKey(Student,models.CASCADE,'claims')
    serial_number = models.IntegerField()

    def __str__(self):
        return str(self.period)

@receiver(pre_save,sender=Claim)
def add_serial_number(sender,instance, **kwargs):
    if instance.serial_number is None:
        instance.serial_number = instance.student.serial
    
    preclaims = instance.student.preclaims
    if len(preclaims.filter(
        event__start_time__lte=instance.start_time, 
        event__end_time__gte=instance.end_time,
        )) >= 1:
        instance.pre_claim_approved = True
    

    
