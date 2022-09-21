from django.db import models
from django.contrib.auth.models import AbstractUser


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
    phone = models.IntegerField(unique=True, null=True, blank =False)
    address = models.CharField(max_length=50)