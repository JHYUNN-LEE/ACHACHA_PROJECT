from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import request
from .models import implement
from .forms import UserForm
from acha_money.models import UserDeal, Posts

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # form.address = request.POST['address'].encode('utf-8')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('http://127.0.0.1:8000')
    else:
        form = UserForm()
    return render(request, 'member/register.html', {'form': form})

def index(request):
    request_list = request.objects.order_by('-create_date')
    context = {'request_list': request_list}
    return render(request, 'member/request.html', context)
# Create your views here.

# def login(request):
#     return render(request, 'member/login.html')


def request(request):
    seller = UserDeal.objects.filter(deal='seller')
    
    # posts = Posts.objects.filter(posts_id_pk = seller.posts_id)
    print(seller)
    print(seller[2].posts_id)
    for post_id in range(len(seller)):
        posts = Posts.objects.filter(posts_id_pk = seller[post_id].posts_id)
    return render(request, 'member/request.html', {'seller':seller, 'posts':'posts'})





