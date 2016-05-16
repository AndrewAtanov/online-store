from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='img/products')
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.title


class Stockroom(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField()
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.title


class Cart(models.Model):
    date = models.DateField(auto_now=True)
    released = models.BooleanField(default=False)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return 'Cart =)'


class Customer(models.Model):
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=30)
    info = models.TextField()

    user = models.OneToOneField(User)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    title = models.CharField(max_length=100)
    categories = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Sale(models.Model):
    title = models.TextField()
    type = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    value = models.FloatField()
    discount = models.FloatField()

    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.title
