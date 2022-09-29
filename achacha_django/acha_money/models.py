from django.db import models
from member.models import customuser
from django.contrib.auth.models import AbstractUser


# Create your models here.
class LostItems(models.Model):
    lost_items_id_pk = models.CharField(primary_key=True, max_length=45)
    get_name = models.CharField(max_length=150, blank=True, null=True)
    get_at = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    get_time = models.CharField(max_length=45, blank=True, null=True)
    get_place = models.CharField(max_length=45, blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    find_place = models.CharField(max_length=45, blank=True, null=True)
    pickup_check = models.CharField(max_length=10, blank=True, null=True)
    center_number = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lost_items'


class Posts(models.Model):
    posts_id_pk = models.AutoField(primary_key=True)
    users_id = models.CharField(max_length=45, blank=True, null=True)
    title = models.CharField(max_length=45, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    parcel = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    lost_items_id = models.CharField(max_length=45, blank=True, null=True)
    img_src = models.ImageField(upload_to='acha_money/', max_length=100, blank=True, null=True)
    get_place = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'


class UserDeal(models.Model):
    deal_id = models.AutoField(primary_key=True)
    users_id = models.CharField(max_length=45)
    posts_id = models.IntegerField()
    deal = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'user_deal'


class PostsDeal(models.Model):
    posts_id_pk = models.IntegerField(primary_key=True)
    contact_check = models.CharField(max_length=10, blank=True, null=True)
    find_check = models.CharField(max_length=10, blank=True, null=True)
    send_check = models.CharField(max_length=10, blank=True, null=True)
    accept_check = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts_deal'