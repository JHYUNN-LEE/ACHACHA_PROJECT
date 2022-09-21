from django.shortcuts import render
from django.core.paginator import Paginator
from . models import LostItems
from hdfs import InsecureClient
from django.views.generic import DetailView
# Create your views here.

default_page = 1

def all_index(request):
    items_per_page = 10
    lost_items_list = LostItems.objects.all()
    paginator = Paginator(lost_items_list, items_per_page)
    page = request.GET.get('page')

    posts = paginator.get_page(page)

    client = InsecureClient('http://localhost:50070/')
    return render(request, 'all_search/all_index.html', {'lost_items_list': lost_items_list,
                                                         'posts': posts})
