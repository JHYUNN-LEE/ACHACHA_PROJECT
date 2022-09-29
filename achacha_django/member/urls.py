from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'member'

urlpatterns = [
    # path('register/', RegisterView.as_view()),
    path('', views.index),
    path('login/', views.LoginView_withlogger.as_view(template_name='member/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('delivery/', views.delivery, name='delivery'),
    path('delivery/delivery_detail/<int:posts_id_pk>/', views.delivery_detail, name='delivery_detail'),
    path('owner/', views.owner, name='owner'),
    path('owner/owner_detail/<int:posts_id_pk>/', views.owner_detail, name='owner_detail'),
    path('mypage/', auth_views.LoginView.as_view(template_name='member/mypageindex.html'), name='mypage'),
    path('auth/', views.SmsSendView.as_view(), name='auth'),
    path('auth_check/', views.SMSVerificationView.as_view(), name='auth_check')
]