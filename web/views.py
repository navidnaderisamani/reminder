from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from json import JSONEncoder
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from web.models import  Expense, User, Token, Income
# Create your views here.

@csrf_exempt
def expense(request):

    #TODO: what if the amout is invlid or token does'nt exist

    print (request.POST)
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    this_user_id = this_user.id
    this_amount = request.POST['amount']
    this_text = request.POST['text']
    now = datetime.now()
    this_dong = request.POST['dong']

    Expense.objects.create(text = this_text, dong = this_dong, date = now,
     amount = this_amount, user_id = this_user_id)


    return JsonResponse({

    'status':'OK',

    },encoder = JSONEncoder)


@csrf_exempt
def income(request):

    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    this_user_id = this_user.id
    this_amount = request.POST['amount']
    this_text = request.POST['text']
    now = datetime.now()
    this_dong = request.POST['dong']

    Income.objects.create(text = this_text, dong=this_dong,
    user_id = this_user_id, amount = this_amount, date = now
    )


    return JsonResponse({
    'status':'OK',
    },encoder = JSONEncoder)
