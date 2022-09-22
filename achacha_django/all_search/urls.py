from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_index),
    path('test/', views.test),
    path('img/', views.imgtest),
    path('base/', views.base),
]