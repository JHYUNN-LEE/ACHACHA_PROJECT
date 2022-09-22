import time
from urllib import request
from django.shortcuts import render, redirect

# 추가
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
import json
from requests.exceptions import ConnectionError
import requests
import base64
from .models import LostItems, Images, UploadedImage
from pyhdfs import HdfsClient
from hdfs import InsecureClient
from hdfs.client import Client

# Create your views here.

# 1_fast_index.html
def fast_index(request):
    return render(request, 'fast_search/1_fast_index.html')

# 2_fast_image.html
def image_search(request):
    return render(request, 'fast_search/2_fast_image.html')

# 3_fast_keyword.html
def keyword_search(request):
    return render(request, 'fast_search/3_fast_keyword.html')

# 2-1.result.html
def uploaded_image(request):
    if request.method == "POST":
        image = request.FILES['uploadfile'] # 업로드 된 이미지 가져오기
        base64_bytes = base64.b64encode(image.read())   # 이미지 데이터 bytes로 변환
        base64_string = base64_bytes.decode('utf-8')    # bytes 데이터 string 변환(bytes자체를 보내면 안 보내져서 일단 str로 변환했음)
        
        category = request.POST.getlist('category') # 선택된 카테고리 데이터 가져오기
        category = category[0]  # 리스트에서 추출
        
        data = {
            'image' : base64_string,
            'category' : category
        }
        
        response = requests.post('http://localhost:5001/', data=data)
        # print(response)

        
        ## flask에서 넘어온 데이터 처리하기
        
        result = response.text
        result = eval(result) # string to list
        
        # image_id 값 추출 / src 찾기 / image 가져오기
        
        image_src_list = []
        # for i in range(0, 3):
        for i in range(len(result)):
            image_name = result[i][:-4]
        
            # mysql - image 테이블에서 src 찾아오기
            image = Images.objects.filter(images_id_fk1 = image_name).values('src')

            image_src = image[0]['src']
            image_src_list.append(image_src)
        # print(image_src_list)
        
        # hdfs 연결하기
        hdfs_client = InsecureClient("http://54.64.90.112:9870/", user="ubuntu")
        hdfs_client.download('/user/ubuntu/text.txt', './media/', overwrite=False, n_threads =1)


        # for r in res:
        #     line=str(r,encoding='utf8')#open     ,str()         
        #     print(line)

    return render(request, 'fast_search/2-1.result.html', {'image_src':image_src})