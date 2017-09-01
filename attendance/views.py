from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from .gcalander import get_classes
from django.views import generic
from json import loads
from .forms import StudentForm, PeriodForm
from django.utils import dateparse
# Create your views here.
def index(request):
    return render(request,'attendance/student_claims.html',{'periodform':PeriodForm, 'studentform':StudentForm})

def class_data(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        batch = Batch.objects.get(pk=int(request.GET.get('batch')))
        if not batch.active:
            return JsonResponse({
        "error":"batch not active"})
        classes = get_classes(date,batch)
        return JsonResponse({
    'number': len(classes),
    'classes':classes
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
