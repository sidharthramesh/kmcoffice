from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,),
    url(r'^class_data$',views.class_data,name='class_data'),
    url(r'^active_batches$',views.active_batches),
    url(r'^status/(?P<roll_no>[0-9]{1,255})/$',views.StatusCheck.as_view(),name='status'),
]
