from django.db import models
from django.utils import timezone


class Product(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='img/products')
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.title
