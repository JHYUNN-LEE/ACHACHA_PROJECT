from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from acha_money.models import Posts
from . models import Alarm
from . models import LostItems
from hdfs import InsecureClient
from django.views.generic import DetailView
# Create your views here.

# logger import 
from . import logger

default_page = 1

def all_index(request):
    # view 로그 추적 
    logger.trace_logger(request)

    items_per_page = 10
    lost_items_list = LostItems.objects.all().order_by('-get_at')
    paginator = Paginator(lost_items_list, items_per_page)
    page = request.GET.get('page')
    max_index = len(paginator.page_range)
    posts = paginator.get_page(page)

    client = InsecureClient('http://54.64.90.112:9870', user="ubuntu")
    
    return render(request, 'all_search/all_index.html', {'lost_items_list': lost_items_list,
                                                         'posts': posts, 'max_index': max_index})
    
    


def all_detail(request, lost_items_id_pk):
    # view 로그 추적 
    logger.trace_logger(request)

    if request.method == "POST":
        users_id = request.user
        category = request.POST['category']
        get_place = request.POST['get_place']
        img_src = request.FILES.get('img_src')
        
        search_item = Posts.objects.create(users_id=users_id,
                            category=category,
                            get_place=get_place,
                            img_src=img_src)
        
        print(search_item.posts_id_pk)
        
        # search_item_list = Posts.objects.filter(posts_id_pk=posts_id_pk)
        # print(search_item_list)
        return redirect('/acha_money/post_search/{}'.format(search_item.posts_id_pk), {'search_item': search_item})
        # return redirect('/acha_money/post/')
    else:
        lost_items_list= LostItems.objects.filter(lost_items_id_pk=lost_items_id_pk)
        return render(request, 'all_search/all_detail.html', {'lost_items_list': lost_items_list})
    
    
def all_alarm(request):
    # view 로그 추적 
    logger.trace_logger(request)
    return render(request, 'all_search/all_alarm.html')


def alarmset(request):
    if request.method == "POST":
        # alarm table
        alarm = Alarm()
        alarm.users_id = request.user.id 
        alarm.phone = f'0{request.user.phone}' #핸드폰번호 앞에 0이 사라지는 것 방지
        alarm.category = request.POST['category']
        alarm.src = f'/home/ubuntu/WEB_SERVICE_ACHACHA/ALARM/images/{request.FILES["img_src"]}'
        # alarm.src = request.FILES["img_src"]
        alarm.turn = 'Y'
        alarm.save()
    return redirect('/')

