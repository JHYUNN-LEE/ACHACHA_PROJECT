from django.db import models
from django.contrib.auth.models import AbstractUser
import requests
from random import randint
from django.utils import timezone
import json
import time
import datetime
import hmac
import base64
import hashlib

# Create your models here.
class request(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

class implement(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

class customuser(AbstractUser):
    # 기본적으로 제공하는 필드 외에 원하는 필드를 적어준다.
    phone = models.IntegerField(unique=True, null=False, blank =False)
    address = models.CharField(max_length=50)

class Authentication(models.Model):
    phone_number = models.CharField('휴대폰 번호', max_length=30)
    auth_number = models.CharField('인증번호', max_length=30)

    class Meta:
        db_table = 'authentications' # DB 테이블명
        verbose_name_plural = "휴대폰인증 관리 페이지" # Admin 페이지에서 나타나는 설명

