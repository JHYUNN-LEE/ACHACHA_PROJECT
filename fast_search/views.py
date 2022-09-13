from django.shortcuts import render

# Create your views here.

def fast_index(request):
    return render(request, 'fast_search/login.html')