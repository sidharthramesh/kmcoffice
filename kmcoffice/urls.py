"""kmcoffice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from venue import views
from venue.forms import LoginForm
from django.contrib.auth import views as authviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$',authviews.login,{'template_name':'venue/login.html','authentication_form':LoginForm},name='login'),
    url(r'^logout/$', authviews.logout, {'next_page': '/list'}, name='logout'),
    url(r'^venue/',include('venue.urls')),
    url(r'^attendance/',include('attendance.urls')),
]
