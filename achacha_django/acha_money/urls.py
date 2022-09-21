from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='acha_money'),
    path('post/', views.post, name='post'),
    path('detail/<int:posts_id_pk>/', views.detail, name='detail'),
]