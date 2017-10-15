from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,),
    url(r'^class_data$',views.class_data,name='class_data'),
    url(r'^active_batches$',views.active_batches),
    url(r'^status/$',views.status_redirect,name='status'),
    url(r'^preclaim/(?P<pk>[0-9]+)/approve/$',views.approve_preclaim, name='approve_preclaim'),
    url(r'^preclaim/(?P<pk>[0-9]+)/disapprove/$',views.delete_preclaim, name='disapprove_preclaim'),
    url(r'^preclaim/(?P<pk>[0-9]+)/forward/$',views.forward_claim,name='forward_preclaim'),
]
