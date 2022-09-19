import time
from urllib import request
from django.shortcuts import render, redirect

# 추가
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from .models import Image
import json


from requests.exceptions import ConnectionError

import requests
import base64

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

# 이미지 fast search
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
        print(type(data))
        response = requests.post('http://localhost:5001/', data=data)
        print(response)
        # result = response.content
        # print(result)
        result = response.text
        print(result)

        
    return render(request, 'fast_search/2-1.result.html')