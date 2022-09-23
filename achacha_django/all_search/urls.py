from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_index),
    path('all_detail/<str:lost_items_id_pk>/', views.all_detail, name="all_detail"),
]

