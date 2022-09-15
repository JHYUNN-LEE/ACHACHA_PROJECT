from django.db import models

# Create your models here.

class Image(models.Model):
    category = models.CharField(max_length = 100)
    image = models.ImageField()
	
    def __str__(self):
        return self.category