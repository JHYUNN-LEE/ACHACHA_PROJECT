from django.shortcuts import render, redirect

# 추가
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from .models import Image


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

# 추가
def uploaded_image(request):
    if request.method == "POST":
        Image.image = request.FILES['uploadfile']
        Image.category = request.POST.getlist('category')
    print(Image.image)
    print(Image.category)
    return render(request, 'fast_search/result.html')