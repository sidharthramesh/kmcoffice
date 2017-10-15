from django.test import TestCase, RequestFactory
from django.utils.timezone import now, timedelta
from .gcalander import get_classes
from .models import *
from django.urls import reverse
import json
import mock
from attendance import views
# Create your tests here.
depts = """Anatomy
Physiology
Biochemistry
Community Medicine
Pathology
Pharmacology
Microbiology
Forensic Medicine
Medicine
ENT
OBG
Opthalmology
Surgery
Paediatrics
Pulmonary Medicine
Orthopaedics
Dental
Dermatology
Neurology"""

class UtilGcalTest(TestCase):
    def setUp(self):
        Batch.objects.create(
            semester=1,
            batch = 'a', 
            calander_id="pi2m3dda6ljkrmh473624vvl9s@group.calendar.google.com")
    
        for dept in depts.splitlines():
            Department.objects.create(name=dept)

    def test_classes(self):
        b = Batch.objects.first()
        classes = get_classes('2017-8-31',b)
        self.assertEqual(len(classes),5)
        #print(classes)
        self.assertIsNotNone(classes[0].get('department'))
        self.assertEqual(classes[0].get('department'),Department.objects.get(name='Pharmacology').pk)
        self.assertIsNotNone(classes[0].get('location'))

class PreClaimModelTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('sid','tornadoalert@gmail.com','Supernova-7')
        rolls = """150101312 Sidharth\n150101222 Someone\n122332232 Another person"""
        event = Event.objects.create(
            name="Test Event",
            start_time = now(),
            end_time = now()+timedelta(days=3))
        with mock.patch('attendance.models.send_email.delay') as mock_email:
            preclaim = PreClaim.objects.create(
                add_roll_numbers=rolls,
                event = event,
                notification_email = 'tornadoalert@gmail.com', 
                faculty_email='faculty@gmail.com',
                )
            kwargs = mock_email.call_args[1]
            self.assertEqual(kwargs['recipient_list'], ['faculty@gmail.com'])
        
    def test_student_exists(self):
        self.assertIsNotNone(Student.objects.first())
        #print(PreClaim.objects.all())
        #print(User.objects.all())
        #print(User.objects.first())
class ProcessClaimsView(TestCase):
    def setUp(self):
        Batch.objects.create(
            semester=1,
            batch = 'a', 
            calander_id="pi2m3dda6ljkrmh473624vvl9s@group.calendar.google.com")
        
        event = Event.objects.create(
            name="Test Event",
            start_time = now(),
            end_time = now()+timedelta(days=3))
        
        preclaim = PreClaim.objects.create(
            add_roll_numbers = "150101312\n150101314",
            event = event
        )
        for dept in depts.splitlines():
            Department.objects.create(name=dept)
        self.factory = RequestFactory()
        dean = User.objects.create_user('dean','dean@dean.com','topsecretpassword123')

    def test_process_claims(self):
        batch = Batch.objects.first()
        date = now()+timedelta(days=1)

        if date.weekday() == 6:
            date = date+ timedelta(days=1)
        date = "{year}-{month}-{day}".format(year=date.year,month=date.month,day=date.day)
        r = self.client.get(reverse('class_data'),{
            'batch': batch.pk,
            'date':date})
        #print('--------------------')
        #print("Get {}".format(reverse('class_data')))
        #print("Get params:", end=' ')
        """print({
            'batch': batch.pk,
            'date':date})
        """
        data = json.loads(r.content.decode())
        l = len(data.get('classes'))
        self.assertEqual(l,data.get('number'))
        classes = data.get('classes')

        #print("Response {}".format(r.status_code))
        #print(r.content.decode())
        for c in classes:
            if c.get('department') is None:
                c['department'] = 1
        #print('--------------------')
        #print("selecting 'department':1 for 'department':null")
        #print('--------------------')
        student_data = {
            'name':'Sidharth R',
            'email':'tornadoalert@gmail.com',
            'roll_no':150101312,
            'serial':104,
            'event':Event.objects.first().pk,
            'selectedClasses': classes
        }
        json_data = json.dumps(student_data)
        r = self.client.post(reverse('class_data'),json_data,
                                content_type="application/json")
        #print("posting to {}".format(reverse('class_data')))
        #print("post payload",end=' ')
        #print(json_data)
        #print()
        #print("got response {}".format(r.status_code))
        #print(r.content.decode())
        #print('--------------------')
        self.assertContains(r,'true')
        claims = Claim.objects.all()
        self.assertEqual(len(claims),l)
        for c in claims:
            self.assertTrue(c.pre_claim_approved)
    def test_forward(self):
        request = self.factory.get(reverse('forward_preclaim',kwargs={'pk':1}))
        request.user = User.objects.create_user('faculty_someone','kjgfhdkjfghdkjf@gmail.com','sdfjskjhsdkjgh')
        with mock.patch('attendance.views.send_email.delay') as mock_email:
            views.forward_claim(request,1)
            _, kwargs = mock_email.call_args
            print(kwargs)

    def test_preclaim(self):
        preclaim = PreClaim.objects.first()
        print(preclaim.get_classes())
    