from django.db import models

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
    
class Alarm(models.Model):
    alarm_id = models.AutoField(primary_key=True)
    users_id = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    src = models.CharField(max_length=100, blank=True, null=True)
    turn = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alarm'