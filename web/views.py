# -*- coding: utf8 -*-
from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from web.models import  Expense, User, Token, Income, Passwordresetcodes
import requests, random, json, string
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.template import RequestContext
from postmark import PMMail
from django.utils.crypto import get_random_string
from django.db.models import Sum, Count
# Create your views here.




random_str = lambda N: ''.join(
    random.SystemRandom().choice(string.ascii_uppercase +
    string.ascii_lowercase + string.digits) for _ in range(N))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def grecaptcha_verify(request):
    if request.method == 'POST':
        response = {}
        data = request.POST
        captcha_rs = data.get('g-recaptcha-response')
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': captcha_rs,
            'remoteip': get_client_ip(request)
        }
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        response["status"] = verify_rs.get("success", False)
        response['message'] = verify_rs.get('error-codes', None) or "Unspecified error."
        return HttpResponse(response)

@csrf_exempt
def register(request):

    if 'requestcode' in request.POST:
    # form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        # is this spam? check reCaptcha
        #user = request.POST['username']
        #email = request.POST['email']
        #password = request.POST['password']

        if not grecaptcha_verify(request):  # captcha was not correct
            context = {
                'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟ کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید. ببخشید که فرم به شکل اولیه برنگشته!'}  # TODO: forgot password
            return render(request, 'register.html', context)

        # duplicate email
        if User.objects.filter(email=request.POST['email']).exists():
            context = {
                'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)
        # if user does not exists
        if not User.objects.filter(username=request.POST['username']).exists():
            code = random_str(28)
            now = datetime.now()
            email = request.POST['email']
            password = make_password(request.POST['password'])
            username = request.POST['username']
            temporarycode = Passwordresetcodes(
                email=email, time=now, code=code, username=username, password=password)
            temporarycode.save()
            message = PMMail(api_key=settings.POSTMARK_API_TOKEN,
                             subject="avtivation email for primatech",
                             sender="info@taktatech.com",
                             to=email,
                             text_body="http://localhost:8000/account/register/?email={}&code={}".format(email,code),
                             tag="account request")
            message.send()
            context = {
                'message': 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'}
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)
    elif 'code' in request.GET:  # user clicked on code
        email=request.GET['email']
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(
                code=code).exists():  # if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username,
             password=new_temp_user.password, email=email)
            this_token = get_random_string(length=48)
            token = Token.objects.create(user=newuser, token=this_token)

            Passwordresetcodes.objects.filter(code=code).delete()
            context = {
                'message': 'اکانت شما ساخته شد. توکن شما {} است. آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد! جدی!'.format(
                    this_token)}
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'index.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)

@csrf_exempt
def login(request):
    # check if POST objects has username and password
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        this_user = get_object_or_404(User, username=username)
        if (check_password(password, this_user.password)):  # authentication
            this_token = get_object_or_404(Token, user=this_user)
            token = this_token.token
            context = {}
            context['result'] = 'ok'
            context['token'] = token
            #context = {'message':'شما با موفقیت وارد شدید'}
            # return {'status':'ok','token':'TOKEN'}
            return JsonResponse(context, encoder=JSONEncoder)
            #return render(request, 'index.html', context)
        else:
            context = {}
            context['result'] = 'error'

            #context = {'message' : 'نام کاربری یا رمز عبور شما اشتباه است لطفا مجددا تلاش کنید'}
            return JsonResponse(context, encoder=JSONEncoder)
            #return render(request, 'login.html', context)


    return render(request, 'login.html')

@csrf_exempt
def report(request):

    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()

    income = Income.objects.filter(user = this_user).aggregate(Sum('amount'))
    expense = Expense.objects.filter(user = this_user).aggregate(Sum('amount'))

    income_count = Income.objects.filter(user = this_user).aggregate(Count('amount'))
    expense_count = Expense.objects.filter(user = this_user).aggregate(Count('amount'))

    context = {}
    context['Income'] = income
    context['Expense'] = expense
    context['income_count'] = income_count
    context['expense_count'] = expense_count
    #TODO: return username

    return JsonResponse(context, encoder = JSONEncoder)



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
    try:
        this_dong = request.POST['dong']
    except:
        this_dong = ''

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


    Income.objects.create(text = this_text,
    user_id = this_user_id, amount = this_amount, date = now
    )


    return JsonResponse({
    'status':'OK',
    },encoder = JSONEncoder)


def index(request):

    context = {'status':'OK'}
    return render(request, 'index.html', context)
