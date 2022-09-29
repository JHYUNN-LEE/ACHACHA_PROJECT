from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.fast_index),
    path('image/', views.image_search, name='image_search'),
    path('image/img_result/', views.uploaded_image, name='image_upload'),
    path('image/img_result/detail/<str:lost_items_id_pk>/', views.image_detail, name='image_detail'),
    path('keyword/', views.keyword_search, name='keyword_search'),
    path('keyword/key_result/', views.find_category_to_es, name='keyword_result'),
    path('keyword/key_result/detail/<str:images_id_pk>/', views.keyword_detail, name='keyword_detail'),
    path('keyword/key_result/all_alarm/', views.all_alarm, name="all_alarm"),
    path('keyword/key_result/all_alarm/alarmset/', views.alarmset, name='alarmset'),
  
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

