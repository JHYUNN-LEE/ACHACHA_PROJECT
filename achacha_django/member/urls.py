from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'member'

urlpatterns = [
    # path('register/', RegisterView.as_view()),
    path('login/', auth_views.LoginView.as_view(template_name='member/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('request/', views.register, name='request'),
    path('register/', views.register, name='register'),
    path('implement/', views.register, name='implement'),
    path('mypage/', auth_views.LoginView.as_view(template_name='member/mypageindex.html'), name='mypage'),
    path('auth/', views.SmsSendView.as_view(), name='auth'),
    path('auth_check/', views.SMSVerificationView.as_view(), name='auth_check')
]