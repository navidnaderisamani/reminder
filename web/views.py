from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def expense(request):

    html = "<html><body><h1> HI To All</h1></body></html>"

    return HttpResponse(html)
