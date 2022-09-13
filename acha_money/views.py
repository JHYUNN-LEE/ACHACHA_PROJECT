from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'base/base.html')

def test(request):
    return render(request, 'acha_money/test.html')