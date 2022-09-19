from django.urls import path
from . import views

urlpatterns = [
    path('', views.fast_index),
    path('image/', views.image_search, name='image_search'), 
    path('keyword/', views.keyword_search, name='keyword_search'),
]