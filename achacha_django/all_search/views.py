from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from . models import LostItems
from hdfs import InsecureClient
from django.views.generic import DetailView
# Create your views here.

default_page = 1

def all_index(request):
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
    lost_items_list= LostItems.objects.filter(lost_items_id_pk=lost_items_id_pk)
    return render(request, 'all_search/all_detail.html', {'lost_items_list': lost_items_list})


