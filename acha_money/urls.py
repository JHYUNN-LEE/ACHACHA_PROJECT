from . import views
from django.urls import path

urlpatterns = [
    path('', views.base),
    path('test/', views.test)
]