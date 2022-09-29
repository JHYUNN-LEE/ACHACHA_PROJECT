from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='acha_money'),
    path('post/', views.post, name='post'),
    path('post_search/<int:posts_id_pk>/', views.post_search, name='post_search'),
    path('detail/<int:posts_id_pk>/', views.detail, name='detail'),
    path('detail_proto/<int:posts_id_pk>/', views.detail_proto, name='detail_proto'),
    path('detail/<int:posts_id_pk>/delete/', views.delete, name='delete'),
    path('detail/<int:posts_id_pk>/update/', views.update, name='update'),
]