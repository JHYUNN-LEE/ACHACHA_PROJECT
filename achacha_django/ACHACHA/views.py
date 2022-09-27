from django.http import HttpResponse
from django.shortcuts import render, redirect

# logger import 
from . import logger

def index(request):
    logger.trace_logger(request)
    return render(request, 'ACHACHA/index.html')

