from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^account/expense/$', views.expense, name='expense'),
    url(r'^account/income/$', views.income, name = 'income'),
    url(r'^account/register/$', views.register, name='register'),
    url(r'^account/login/$', views.login, name='login'),
    url(r'^account/report/$', views.report, name='report'),
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index, name='home'),


]
