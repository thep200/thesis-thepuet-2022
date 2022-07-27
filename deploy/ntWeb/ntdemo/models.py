from django.db import models

# Create your models here.
class ImageNT(models.Model):
    # caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.caption
