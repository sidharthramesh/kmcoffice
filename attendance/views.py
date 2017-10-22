from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .gcalander import get_classes
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from json import loads
from .forms import StudentForm, PeriodForm
from django.utils import dateparse
from django.contrib.auth.decorators import permission_required
from .forms import ConfirmForm, StatusForm
from .tasks import send_email
from django.contrib.auth.decorators import user_passes_test
from venue.quotes import get_random_quote
import csv
# Create your views here.

def home(request):
    return render(request,'home.html',{})

def index(request):
    return render(request,'attendance/student_claims.html',{'periodform':PeriodForm, 'studentform':StudentForm})
@csrf_exempt
def class_data(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        batch = Batch.objects.get(pk=int(request.GET.get('batch')))
        if not batch.active:
            return JsonResponse({
        "error":"batch not active"})
        classes = get_classes(date,batch)
        print(classes)
        return JsonResponse({
    'number': len(classes),
    'classes': classes
    })

    if request.method == 'POST':
        return process_claims(request)

def active_batches(request):
    active_batches = Batch.objects.filter(active=True)
    active_batches = [str(batch).upper() for batch in active_batches]
    return JsonResponse({
'active_batches':active_batches})

def process_claims(request):
    #print("Got a claim")
    data = loads(request.body.decode('utf-8'))
    #print(data)
    student_data = {k:data[k] for k in ['name','roll_no','email','serial','event']}
    #print(student_data)
    student_form = StudentForm(student_data)

    if student_form.is_valid():
        pass
        #print("Student Form valid")
        student_data = student_form.cleaned_data
        student,_ = Student.objects.get_or_create(roll_no=student_data['roll_no'])
        student.name = student_data.get('name')
        student.email = student_data.get('email')
        student.serial = student_data.get('serial')
        #print(student)
        student.save()
    else:
        #print("Student form invalid")
        return JsonResponse({
    'success':False,
    "errors":student_form.errors
    })
    errors = []
    clean_classes = []
    for period in data.get('selectedClasses'):
        p = PeriodForm(period)
        if p.is_valid():
            c = p.cleaned_data
            clean_classes.append(c)
        else:
            errors.append(p.errors)

    if len(errors) > 0:
        return JsonResponse({"success":False, "errors":errors})
    #print((clean_classes))
    for c in clean_classes:

            p,_ = Period.objects.get_or_create(
                batch=c['batch'],
                name=c['name'],
                start_time=c['start'],
                end_time=c['end'],
                department = c['department'])

            claim = Claim.objects.create(
                event = student_data.get('event'),
                period = p,
                student = student,
            )

    return JsonResponse({"success":True})

def status_redirect(request):
    if request.GET.get('roll_no'):
        queryset = Claim.objects.filter(student__roll_no=request.GET.get('roll_no'))
        return render(request,'attendance/status.html',{'claims':queryset})
    else:
        return render(request,'attendance/status_form.html',{'form':StatusForm})

def download_claims(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_claims.csv"'

    writer = csv.writer(response)
    writer.writerow(["Serial","Reg no","Name","Date","Class missed","Time","Event","Semester"])
    for claim in Claim.objects.all():
        print(claim.period)
        writer.writerow([claim.student.serial, claim.student.roll_no, claim.student.name, claim.period.start_time.strftime('%d %B %Y'), claim.period.name, "{} to {}".format(claim.period.start_time.strftime("%-I:%M %p"), claim.period.end_time.strftime("%-I:%M %p")), claim.event.name, claim.period.batch.semester])
    return response

@permission_required('attendance.preclaim_dean_approve')
def approve_preclaim(request, pk):
    if request.method == 'GET':
        preclaim = PreClaim.objects.get(pk=int(pk))
        preclaim.dean_approved=True
        preclaim.save()
        send_email.delay("PreClaim Approved", "The PreClaim has been approved.",'sidharth@mail.manipalconnect.com',[preclaim.notification_email])

        return render(request,'attendance/approved.html',{'preclaim':preclaim})

@permission_required('attendance.preclaim_dean_approve')
def delete_preclaim(request,pk):
    preclaim = PreClaim.objects.get(pk=int(pk))
    if request.method == 'GET':
        return render(request,'attendance/confirm.html',{'preclaim':preclaim,'form':ConfirmForm})

    if request.method == 'POST':

        f = ConfirmForm(request.POST)
        if f.is_valid():
            reason = f.cleaned_data.get('reason')
        preclaim.delete()
        send_email.delay("PreClaim Rejected", reason ,[preclaim.notification_email])
        return render(request,'attendance/dissapproved.html',{'reason':reason,'preclaim':preclaim})

def test_if_facluty(user):
    if user.username.split('_')[0] == 'faculty':
        return True
    else:
        return False
@user_passes_test(test_if_facluty)
def forward_claim(request, pk):
    preclaim = PreClaim.objects.get(pk=int(pk))
    user = User.objects.get(username='dean')
    login_token = utils.get_parameters(user)
    approve_link = reverse('approve_preclaim',kwargs={'pk':pk})
    approve_link = add_auth_token(approve_link,login_token)
    #print(approve_link)
    disapprove_link = reverse('disapprove_preclaim',kwargs={'pk':pk})
    disapprove_link = add_auth_token(disapprove_link,login_token)
    #print(disapprove_link)
    url = 'http://kmcoffice.herokuapp.com'
    approve_link = url+approve_link
    disapprove_link = url+disapprove_link
    body = render_to_string('attendance/email/dean.html',{'approve':approve_link,'disapprove':disapprove_link,'preclaim':preclaim,'quote':get_random_quote})
    #print(body)
    send_email.delay("PreClaim Approval",'',from_email='attendance@mail.manipalconnect.com',recipient_list=[user.email], html_message=body)
    return render(request,'attendance/approved.html',{'preclaim':preclaim})
