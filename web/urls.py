from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bill/expense/$', views.expense, name='expense'),

]
