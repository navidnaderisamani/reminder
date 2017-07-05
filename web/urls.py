from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^account/expense/', views.expense, name='expense'),
    url(r'^account/income/', views.income, name = 'income'),


]
