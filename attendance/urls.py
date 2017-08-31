from django.conf.urls import url
from . import views
urlpatterns = [
    url('^$',views.index,),
    url('^class_data$',views.class_data,name='class_data'),
    url('^active_batches$',views.active_batches)
]
