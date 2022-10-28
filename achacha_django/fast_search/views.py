import time
from unicodedata import category
from urllib import request
from django.shortcuts import render, redirect

# 추가
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, Page

# models.py
from .models import LostItems, Images, Alarm
from acha_money.models import UserDeal

# python edit import
import json
from requests.exceptions import ConnectionError
import requests
import base64
from datetime import datetime
import pandas as pd 

from .models import LostItems, Images

# pip install elasticsearch
from elasticsearch import Elasticsearch

# pip install hdfs
from hdfs import InsecureClient
from hdfs.client import Client
from django.core.paginator import Paginator

# logger import 
from . import logger


# acha_money connect with Posts 
from acha_money.models import Posts

# Create your views here.

# 1_fast_index.html
def fast_index(request):
    logger.trace_logger(request) # view 로그 추적 
    return render(request, 'fast_search/1_fast_index.html')

# 2_fast_image.html
def image_search(request):
    logger.trace_logger(request) # view 로그 추적 
    return render(request, 'fast_search/2_fast_image.html')

# 3_fast_keyword.html
def keyword_search(request):
    logger.trace_logger(request) # view 로그 추적 
    return render(request, 'fast_search/3_fast_keyword.html')

# 2-1.result.html
def uploaded_image(request):

    logger.trace_logger(request) # view 로그 추적 

    if request.method == "POST":
        image = request.FILES['uploadfile'] # 업로드 된 이미지 가져오기
        bytes_image = base64.b64encode(image.read())   # 이미지 데이터 bytes로 변환
        str_image = bytes_image.decode('utf-8')    # bytes to str (bytes자체를 보내면 값이 안 넘어가서, str으로 변환)
        
        category = request.POST.get('category') # 선택된 카테고리 데이터 가져오기
        
        data = {
            'image' : str_image,
            'category' : category
        }
        
        # insert 로그 추적 
        log_context = {
            'image':str(image),
            'category' : category
        }
        logger.trace_logger_context(request, log_context)

        global response
        response = requests.post('http://localhost:5001/', data=data)
                    
    ## flask에서 넘어온 데이터 처리하기
        
    result = response.text
    result = eval(result) # string to list
    
    # 관리번호 값 추출 / src 찾기 / image 가져오기
    
    image_src_list = []
    detail_info = []

    for i in range(len(result)):
        image_id = result[i][:-4] # 관리번호 값 추출
    
        # mysql - image 테이블에서 src 찾아오기
        image = Images.objects.filter(images_id_fk1 = image_id).values('src')
        
        if image.exists():
            image_src = image[0]['src']
            image_src_list.append(image_src)
            
            # mysql - 분실물명, 날짜 가져오기
            lost_item_data = LostItems.objects.filter(lost_items_id_pk = image_id)[0]
            detail_info.append(lost_item_data)

        else : 
            pass
    
    # AWS에서 실행, hdfs 접속
    client = InsecureClient("http://호스트 입력:9870/", user="ubuntu")
    
    # 유사 이미지 output for문으로 대조하여 이미지 가져오기 (가져온 이미지 list : download_list)
    ## image_src_list : /user/ubuntu/service_image/XXXX.jpg
    download_list=[]
    for img in image_src_list:
                download = client.download(img, './media/result_image/', overwrite=True, n_threads = 1)
                download
                media_route = download[-43:]
                download_list.append(media_route)

    object_list = zip(download_list, detail_info)
    converted_list = list(object_list)
    
    paginator = Paginator(converted_list, 6)
    page = request.GET.get('page', 1)
    max_index = len(paginator.page_range)
    posts = paginator.get_page(page)
    
    context = {
        "list" : converted_list,
        "posts" : posts,
        "max_index" : max_index
    }
    return render(request, 'fast_search/2-1_image_result.html', context)

# 2-2_image_detail.html
def image_detail(request, lost_items_id_pk):
    logger.trace_logger(request)
    
    detail_info = LostItems.objects.filter(lost_items_id_pk = lost_items_id_pk)[0]
    
    image_src = f'/media/result_image/{lost_items_id_pk}.jpg'
    
    context = {"image_src" : image_src,
               "detail_info" : detail_info} 
    
    return render(request, 'fast_search/2-2_image_detail.html', context)

# es  find hits 함수 
def trans_source(hits):
    hits_list = []
    
    for hit in hits:
        hits_list.append(hit['_source'])
    return hits_list


# 3-1_keyword_result.html
def find_category_to_es(request):

    logger.trace_logger(request) # view 로그 추적 
    if request.method == 'GET': 
        insert_category = request.GET.get("insert_category")
        insert_color = request.GET.get("insert_color")
        insert_date = request.GET.get("insert_date")
        
    
    #print(insert_category, insert_color, insert_date)
    #print(insert_category, insert_color, insert_date)

    es = Elasticsearch("http://호스트 입력:9200")

    res = es.search(index='lost112', size=10000,
                query = {    
                    "bool": {
                        "must": [
                            {"match": {"category" : insert_category}},
                            {"match": {"content.nori_discard": insert_color}},
                            {"range": {
                                "get_at": {
                                    "gte": insert_date,
                                    "lt": "now"
                                        }
                                    }
                                }
                            ]
                        } 
                    }
                )

    hits = res['hits']['hits']
    
    
    datas = trans_source(hits)
    
    page = request.GET.get('page')
    paginator = Paginator(datas, 10)
    

    #print(datas) 
    max_index = len(paginator.page_range)
    posts = paginator.get_page(page)
   
    
    context = {'datas' : datas,
                'insert_category': insert_category,
                'insert_color' : insert_color,
                'insert_date' : insert_date,
                'max_index' : max_index,
                'posts' : posts}

    log_context = {
            'insert_category':insert_category,
            'insert_color' : insert_color,
            'insert_date' : insert_date
        }

    logger.trace_logger_context(request, log_context)

    return render(request, 'fast_search/3-1_keyword_result.html', context)

def all_alarm(request):
    return render(request, 'all_search/all_alarm.html')

# 3-2_keyword_detail.html
def keyword_detail(request, images_id_pk):
    if request.method == "POST":

        users_id = str(request.user)
        category = request.POST.get('category')
        get_place = request.POST.get('get_place')

        img_src = request.FILES.get('img_src')
        
        lost_items_id = images_id_pk
        
        #print(users_id, category, get_place, img_src)

        search_item = Posts.objects.create(users_id=users_id,
                    category=category,
                    get_place=get_place,
                    img_src=img_src,
                    lost_items_id = lost_items_id
        ) 
        deal= request.POST['deal']
        #print(deal)
        user_deal = UserDeal.objects.create(users_id= users_id,
                                        posts_id= search_item.posts_id_pk,
                                        deal= deal)
                                        
        context = {
            'search_item': search_item,
        }

        return redirect('/acha_money/post_search/{}'.format(search_item.posts_id_pk), context)

    else:
        logger.trace_logger(request)# view 로그 추적 
        
        es = Elasticsearch("http://호스트 입력:9200")

        res = es.search(index='lost112', size=1,
                    body = { "query":  
                                {"match": {"images_id_pk" : images_id_pk}},
                                            }
                )
        
        hits = res['hits']['hits']
        datas = trans_source(hits)
        context = {'datas' : datas}

        #print(datas)
        
        return render(request, 'fast_search/3-2_keyword_detail.html', context)

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