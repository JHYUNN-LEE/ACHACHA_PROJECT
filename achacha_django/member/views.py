from django.shortcuts import render, redirect

# Create your views here.

def login(request):
    return render(request, 'member/login.html')