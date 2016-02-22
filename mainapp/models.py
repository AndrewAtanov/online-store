from django.db import models
from django.utils import timezone


class MainCarousel(models.Model):
    title = models.CharField(max_length=200)
    url = models.TextField()
