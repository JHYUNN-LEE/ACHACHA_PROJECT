from django.shortcuts import render

# Create your views here.

def money_index(request):
    return render(request, 'acha_money/test.html')

