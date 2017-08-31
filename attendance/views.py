from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from .gcalander import get_classes
from django.views import generic
from json import loads
from .forms import StudentForm, PeriodForm
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
    data = loads(request.body.decode('utf-8'))
    student_data = {data[k] for k in ['name','roll_no','email','serial','event']}
    student_form = StudentForm(student_data)
    if not student_form.is_valid():
        return JsonResponse({
    'success':False,
    "errors":student_form.errors
    })
    
    student_data = student_form.cleaned_data
    student = Student.objects.get_or_create(roll_no=student_data['roll_no'])
    student.email = student_data['email']
    student.serial = student_data['serial']
    student.save()

    batch = student_data['batch']
    errors = []
    for period in data['selectedClasses']:
        p = PeriodForm(period)
        if p.is_valid():
            c = p.cleaned_data
            p = Period.objects.get_or_create(
                batch=Batch.objects.get(name=c['batch']),
                name=c['name'],
                start_time=c['start_time'],
                end_time=c['end_time'],
                department = c['department'])

            claim = Claim.create(
                event = student_data['event'],
                period = p,
                student = student,
            )
        else:
            errors.append(p.errors)
        if len(errors) > 0:
            return JsonResponse({"success":False, "errors":errors})
    
    return JsonResponse({"success":True})
