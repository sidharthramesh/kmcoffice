from celery import shared_task, task
import requests, datetime
from django.core.mail import send_mail as mail
from django.core.mail import EmailMessage
from io import StringIO
from django.utils import timezone
import csv
from kmcoffice.settings import TO_EMAIL
@task
def add(a=3,b=1):
    return a+b

@task
def ping():
    r = requests.post("https://requestb.in/1dvp3ch1",{"hello":"World"})
    return r.status_code

@shared_task
def send_email(*args,**kwargs):
    return mail(*args,**kwargs)

@shared_task
def generate_csv():
    from attendance.models import Claim
    csvfile = StringIO()
    writer = csv.writer(csvfile)

    writer.writerow(["Serial","Reg no","Name","Date","Class missed","Department","Time","Event","Semester"])
    for claim in Claim.objects.all():
        print(claim.period)
        delta = timezone.timedelta(minutes=(5*60)+30)
        start_time = claim.period.start_time + delta
        end_time = claim.period.end_time + delta
        writer.writerow([claim.student.serial, claim.student.roll_no, claim.student.name, start_time.strftime('%d %B %Y'), claim.period.name, claim.period.department.name, "{} to {}".format(start_time.strftime("%-I:%M %p"), end_time.strftime("%-I:%M %p")), claim.event.name, claim.period.batch.semester])
    
    message = EmailMessage("All Claims {}".format(datetime.datetime.today().strftime("%d %b %Y")),"Claims are attached","tornadoalert@gmail.com",[TO_EMAIL])
    message.attach('all_clais.csv', csvfile.getvalue(), 'text/csv')
    message.send()