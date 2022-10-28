from enum import auto
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import request
from .models import implement
from .forms import UserForm
from acha_money.models import Posts, UserDeal


# Python
import json, requests, time, random

# Django
from django.views import View
from django.http import JsonResponse
from .utils import make_signature
from .models import Authentication
from acha_money.models import UserDeal
from acha_money.models import Posts

# logger import 
from . import logger

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView



class LoginView_withlogger(LoginView): 
    def log_check(request):
        logger.trace_logger(request)


def register(request):
    logger.trace_logger(request) # view 로그 추적 

    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            # form.address = request.POST['address'].encode('utf-8')
            form.save()
            

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('http://54.64.90.112:8000')
    else:
        form = UserForm()
        
    return render(request, 'member/register.html', {'form': form})

def index(request):
    logger.trace_logger(request) # view 로그 추적 
    request_list = request.objects.order_by('-create_date')
    context = {'request_list': request_list}
    return render(request, 'member/request.html', context)


def owner(request):
    logger.trace_logger(request) # view 로그 추적 
    user_name = request.user
    posts = Posts.objects.raw("SELECT * FROM posts join user_deal \
                             on posts.posts_id_pk = user_deal.posts_id \
                        where user_deal.deal = 'owner' and user_deal.users_id= %s", [user_name])
    # post = Posts.objects.filter(users_id=request.user)
    # post = post.extra(tables=['user_deal'], where=['posts.posts_id_pk=user_deal.posts_id'])
    # print(post)
    return render(request, 'member/owner.html', {'posts': posts})


# class requestList():
#     template_name = "member/request.html"
#     context_object_name = 'request'
#
#     def get_queryset(self, **kwargs):
#         queryset = UserDeal.objects.filter(users_id = self.request.session.get('user'))
#         return queryset
#
# def request(self, request):
#     seller = UserDeal.objects.filter(users_id=self.request.session.get('user'))
#     return render(request, 'member/request.html', {'seller': seller})



def delivery(request):

    
    logger.trace_logger(request) # view 로그 추적 

    user_name = request.user
    posts = Posts.objects.raw("SELECT * FROM posts join user_deal \
                             on posts.posts_id_pk = user_deal.posts_id \
                        where user_deal.deal = 'delivery' and user_deal.users_id=%s", [user_name])

    # post = post.extra(tables=['user_deal'], where=['posts.posts_id_pk=user_deal.posts_id']).distinct()
    return render(request, 'member/delivery.html', {'posts': posts})



# Create your views here.

# def login(request):
#     return render(request, 'member/login.html')




# 인증번호 발송
class SmsSendView(View):
    def send_sms(self, phone_number, auth_number):
        sid = "ncp:sms:kr:292968693103:achacha_auth"
        sms_uri = "/sms/v2/services/{}/messages".format(sid)
        sms_url = "https://sens.apigw.ntruss.com{}".format(sms_uri)
            
        acc_key_id  = "D3HFVghtWIESI6SSXmlE"          
        timestamp = str(int(time.time() * 1000))  

        body = {
            "type": "SMS", 
            "contentType": "COMM",
            "from": "01028820828", 
            "content": f"[아차차 인증번호:{auth_number}]", 
            "messages": [{"to": f"{phone_number}"}] 
        }
        response = requests.post(
        sms_url, data=json.dumps(body),
        headers={"Content-Type": "application/json; charset=utf-8",
                "x-ncp-apigw-timestamp": timestamp,
                "x-ncp-iam-access-key": acc_key_id,
                "x-ncp-apigw-signature-v2": make_signature(timestamp)
                }
         )
        return response.text
        
    def post(self, request):
        # data = json.loads(request.body)
        data = json.loads(request.body)
        print("Phone : ", data)
        if Authentication.DoesNotExist: # DB 입력 로직 작성
            input_mobile_num = data
            auth_num = random.randint(10000, 100000)
            Authentication.objects.create(
                phone_number=input_mobile_num,
                auth_number=auth_num,
            ).save()
            self.send_sms(phone_number=input_mobile_num, auth_number=auth_num)
            return JsonResponse({'message': '인증번호 발송 및 DB 입력완료'}, status=200)

        else:
            auth_mobile = Authentication.objects.get(phone_number=input_mobile_num)
            auth_mobile.auth_number = auth_num
            auth_mobile.save()
            self.send_sms(phone_number=data, auth_number=auth_num)
            return JsonResponse({'message': '인증번호 발송완료'}, status=200)


# 인증번호 확인
class SMSVerificationView(View):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        auth_number = request.POST.get('auth_number')
        print("phone_number : ", phone_number, "| auth_number : ", auth_number)
        try:
            verification = Authentication.objects.get(phone_number=phone_number)

            if verification.auth_number == auth_number:
                verification.delete() # 인증된 내역은 삭제
                return JsonResponse({'message': '인증 완료되었습니다.'}, status=200)

            else:
                return JsonResponse({'message': '인증 실패입니다.'}, status=400)

        except Authentication.DoesNotExist:
            return JsonResponse({'message': '해당 휴대폰 번호가 존재하지 않습니다.'}, status=400)
        
        
        
def delivery_detail(request, posts_id_pk):
    posts = Posts.objects.filter(posts_id_pk=posts_id_pk)
    deal = posts.values()
    context = {
        "posts": posts,
        "deal": deal,
    }
    return render(request, 'member/delivery_detail.html', context)

def owner_detail(request, posts_id_pk):
    posts = Posts.objects.filter(posts_id_pk=posts_id_pk)
    deal = posts.values()[0]
    context = {
        "posts": posts,
        "deal": deal,
    }
    return render(request, 'member/owner_detail.html', context)

