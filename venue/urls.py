from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.BookEvent.as_view(),name="book"),
    url(r'^list/$',views.EventList.as_view(),name="list"),
    url(r'^list/(?P<pk>[0-9]+)',views.EventDetail.as_view(),name='detail'),
    url(r'^thankyou$',views.Thankyou.as_view(),name='thankyou'),
    url(r'^approve/(?P<pk>[0-9]+)',views.approve_booking,name='approve_booking'),
    url(r'^disapprove/(?P<pk>[0-9]+)',views.delete_booking,name='disapprove_booking'),
]
