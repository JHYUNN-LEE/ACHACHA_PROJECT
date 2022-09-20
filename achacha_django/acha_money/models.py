from django.db import models

# Create your models here.
class LostItems(models.Model):
    lost_items_id_pk = models.CharField(primary_key=True, max_length=45)
    get_name = models.CharField(max_length=150, blank=True, null=True)
    get_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    get_place = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    find_place = models.CharField(max_length=45, blank=True, null=True)
    pickup_check = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lost_items'


class Posts(models.Model):
    posts_id_pk = models.AutoField(primary_key=True)
    users_id_fk1 = models.ForeignKey('Users', models.DO_NOTHING, db_column='users_id_fk1')
    title = models.CharField(max_length=45, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    parcel = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    lost_items_id_fk2 = models.ForeignKey(LostItems, models.DO_NOTHING, db_column='lost_items_id_fk2')
    img_src = models.ImageField(upload_to='acha_money/', max_length=100, blank=True, null=True)
    get_place = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'


class Users(models.Model):
    users_id_pk = models.CharField(primary_key=True, max_length=45)
    name = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    addr = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
