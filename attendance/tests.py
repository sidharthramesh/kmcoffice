from django.test import TestCase
from datetime import datetime, timedelta
from .gcalander import get_classes
from .models import *
from django.url
# Create your tests here.
class UtilGcalTest(TestCase):
    def setUp(self):
        Batch.objects.create(name="1st Semester Batch A", calander_id="pi2m3dda6ljkrmh473624vvl9s@group.calendar.google.com")


    def test_classes(self):
        b = Batch.objects.first()
        classes = get_classes('2017-8-31',b)
        self.assertEqual(len(classes),5)
        self.assertIsNotNone(classes[0].get('department'))
        self.assertEqual(classes[0].get('department'),'Pharmacology')
        self.assertIsNotNone(classes[0].get('location'))

class PreClaimModelTest(TestCase):
    def setUp(self):
        rolls = """150101312 Sidharth\n150101222 Someone\n122332232 Another person"""
        event = Event.objects.create(
            name="Test Event",
            start_time = datetime.utcnow(),
            end_time = datetime.utcnow()+timedelta(days=3))
        
        preclaim = PreClaim.objects.create(
            add_roll_numbers=rolls,
            event = event,
            )
        
    def test_student_exists(self):
        self.assertIsNotNone(Student.objects.first())
    

class ProcessClaimsView(TestCase):
    def setUp(self):
        Batch.objects.create(name="1st Semester Batch A", calander_id="pi2m3dda6ljkrmh473624vvl9s@group.calendar.google.com")
    
    def test_process_claims(self):

        json = """{"name":"Sid","email":"tornadoalert@gmail.com","rollNumber":"150101312","serialNumber":"104","batch":"1st Semester Batch A","selectedClasses":[{"date":"2017-08-16","department":"Biochemistry","end_time":"10:30 AM","id":61,"name":"Biochemistry","start_time":"09:30 AM"},{"date":"2017-08-16","department":"Anatomy","end_time":"03:00 PM","id":60,"name":"Anatomy demonstration/ histology","start_time":"02:00 PM"}],"event":"Testing"}"""
        r = self.client.get(,{
            'batch': "1st Semester Batch A",
            'date':'2017-08-09'
        })
        print(r.content)