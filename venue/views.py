from django.shortcuts import render, redirect
from django.views import generic
from .models import Booking
from .forms import VenueBookingForm, StatusForm

# Create your views here.

class BookEvent(generic.edit.CreateView):
    success_url = '/thankyou'
    form_class = VenueBookingForm
    template_name = 'venue/booking_form.html'

class Thankyou(generic.TemplateView):
    template_name = 'venue/thankyou.html'

class EventList(generic.ListView):
    model = Booking
    context_object_name = 'bookings'
    template_name = 'venue/list.html'
    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['approved'] = Booking.objects.filter(status='3').order_by('-start_time')
        context['denied'] = Booking.objects.filter(status='2').order_by('-start_time')
        context['awaiting'] = Booking.objects.filter(status='1').order_by('-start_time')
        return context

class EventDetail(generic.UpdateView):
    model = Booking
    fields = ['status']
    template_name = 'venue/detail.html'
    success_url = '/list' 
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(EventDetail, self).dispatch(
            request, *args, **kwargs)

    