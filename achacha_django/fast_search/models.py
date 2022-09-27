from django.db import models

# Create your models here.

# class Image(models.Model):
#     category = models.CharField(max_length = 100)
#     image = models.ImageField(upload_to="upload_image/")
	
#     def __str__(self):
#         return self.category

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
        
        
class Images(models.Model):
    images_id_pk = models.AutoField(primary_key=True)
    images_id_fk1 = models.CharField(max_length=45)
    src = models.CharField(max_length=100, blank=True, null=True)
    yolo_category = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'
        
class UploadedImage(models.Model):
    # uploaded_image = models.TextField()
    uploaded_image = models.ImageField(upload_to="upload_image/")
    category = models.CharField(max_length=15)
    uploaded_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uploaded_image'

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