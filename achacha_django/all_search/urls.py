from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_index),
    path('all_detail/<str:lost_items_id_pk>/', views.all_detail, name="all_detail"),
    path('all_alarm/', views.all_alarm, name="all_alarm"),
    path('all_alarm/alarmset/', views.alarmset, name='alarmset'),
]

