from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pytils import translit
from picklefield.fields import PickledObjectField
from django.core.cache import cache
from mysite.settings import TIME


class Category(models.Model):
    title = models.CharField(max_length=100)
    categories = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    translit_title = models.CharField(max_length=200, default='')

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.translit_title = translit.slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='img/products')
    description = models.TextField()
    price = models.IntegerField()

    category = models.ForeignKey(Category, null=True)

    translit_title = models.CharField(max_length=200, default='')

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.translit_title = translit.slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Stockroom(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField()
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.title


class Customer(models.Model):
    full_name = models.CharField(max_length=200, default='')
    address = models.TextField(default='')
    phone_number = models.CharField(max_length=30, default='')
    info = models.TextField(default='')

    user = models.OneToOneField(User, null=True)

    def __str__(self):
        return self.full_name


def create_customer(user):
    """ Создает объект Customer для User """
    Customer(user=user, full_name=user.last_name).save()


class Cart(models.Model):
    date = models.DateField(auto_now=True)
    released = models.BooleanField(default=False)
    # products = models.ManyToManyField(Product, null=True)
    total_price = models.IntegerField(default=0)
    quantity = PickledObjectField()

    token = models.CharField(max_length=100, null=True)
    customer = models.ForeignKey(Customer, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.quantity = {}

        _cache = kwargs.get('_cache', False)
        kwargs.pop('_cache', None)

        super(Cart, self).save(*args, **kwargs)

        self.total_price = 0
        for el in self.productcart_set.all():
            self.total_price += el.product.price * el.quantity

        super(Cart, self).save(*args, **kwargs)

        if _cache:
            if self.customer:
                cache.set('cart_customer-' + str(self.customer.id), self, TIME['HOUR'])
            else:
                cache.set('cart_token-' + self.token, self, TIME['HOUR'])

    def __str__(self):
        return 'Cart'


class ProductCart(models.Model):
    product = models.ForeignKey(Product)
    cart = models.ForeignKey(Cart)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s in %s' % (self.product, self.cart)


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
