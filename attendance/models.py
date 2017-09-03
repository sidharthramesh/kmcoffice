from django.db import models

from django.shortcuts import reverse
from venue.models import Venue
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from sesame import utils
from django.contrib.auth.models import Permission, User
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
    notification_email = models.EmailField()
    students = models.ManyToManyField(Student,'preclaims')

    def __str__(self):
        return str(self.event) + ' Preclaim'
    def days(self):
        delta = self.event.end_time - self.event.start_time
        return delta.days
    def get_classes(self):
        from . import gcalander as gc
        batches = Batch.objects.filter(active=True)
        delta = self.event.end_time - self.event.start_time
        #print(delta)
        dates = [self.event.start_time.date() + timezone.timedelta(days=i) for i in range(delta.days+1)]
        classes = []
        for batch in batches:
            for date in dates:
                d = date.strftime('%Y-%m-%d')
                cl = gc.get_classes(d,batch)
                #print(cl)
                for c in cl:
                    if not c.get('name') in classes:
                        classes.append(c.get('name'))
        return classes 

    class Meta:
        permissions = (
            ('preclaim_dean_approve','Dean approval for Preclaim'),
        )
def users_with_perm(perm_name):
    return User.objects.filter(
        is_superuser=True ,
        user_permissions__codename=perm_name ,
        groups__permissions__codename=perm_name).distinct()

def add_auth_token(link,login_token):
    link+='?method=magic&url_auth_token={}'.format(login_token['url_auth_token'])
    return link
@receiver(post_save, sender=PreClaim)
def create_claims(sender, instance, created, **kwargs):
    #print("Running post save for PreClaim")
    instance.students.clear()
    roll_nos = [line.split(' ')[0] for line in instance.add_roll_numbers.split('\n')]
    for roll in roll_nos:
        student = Student.objects.get_or_create(roll_no=int(roll))
        instance.students.add(student[0])
    
    if created:
        users = [user for user in User.objects.all() if user.has_perm('attendance.preclaim_dean_approve')]
        for user in users:
            login_token = utils.get_parameters(user)
            approve_link = reverse('approve_preclaim',kwargs={'pk':instance.pk})
            approve_link = add_auth_token(approve_link,login_token)
            #print(approve_link)
            disapprove_link = reverse('disapprove_preclaim',kwargs={'pk':instance.pk})
            disapprove_link = add_auth_token(disapprove_link,login_token)
            #print(disapprove_link)
            approve_link = 'http://localhost:8000'+approve_link
            disapprove_link = 'http://localhost:8000'+disapprove_link
            body = render_to_string('attendance/email/dean.html',{'approve':approve_link,'disapprove':disapprove_link,'preclaim':instance})
            #print(body)
            send_mail("PreClaim Approval",'',from_email='sidharth@mail.manipalconnect.com',recipient_list=[user.email], html_message=body)



class Claim(models.Model):
    event = models.ForeignKey(Event,models.CASCADE,'claims')
    period = models.ForeignKey(Period,related_name='claims')
    #pre_claim_approved = models.BooleanField(default=False)
    js_approved = models.BooleanField(default=False)
    sis_approved = models.BooleanField(default=False)
    student = models.ForeignKey(Student,models.CASCADE,'claims')
    serial_number = models.IntegerField()
    
    def __str__(self):
        return str(self.period)
    def pre_claim_approved(self):
        preclaims = self.student.preclaims
        preclaims = preclaims.filter(
            event__start_time__lte=self.event.start_time, 
            event__end_time__gte=self.event.end_time,
            )
        if len(preclaims) >= 1:
            for preclaim in preclaims:
                if preclaim.dean_approved:
                    return True
        return False
    pre_claim_approved.boolean = True

    def date(self):
        return self.period.start_time.date()
    
    def name(self):
        return self.student.name
    class Meta:
        permissions = (
            ('claim_js_approve','Can approve the claim with js status'),
            ('claim_sis_approve','Can approve the claim with sis status'),
            )
@receiver(pre_save,sender=Claim)
def add_serial_number(sender,instance, **kwargs):
    if instance.serial_number is None:
        instance.serial_number = instance.student.serial
    
    
    

