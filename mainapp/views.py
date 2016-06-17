from django.shortcuts import render
from django.http import HttpResponse
from paypal.standard.forms import PayPalPaymentsForm
from .models import Product, Category, Cart, ProductCart
import random
from datetime import datetime
from mainapp.cart import get_or_create_cart
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from mysite.settings import TIME

random.seed(datetime.now())

# Create your views here.

# Раскоментировать по надобности
# @cache_page(TIME['DAY'])
def main(request):
    context = {}
    context["auth"] = True
    if not request.user.is_authenticated():
        context["auth"] = False
    return render(request, 'mainapp/main.html', context)


def catalog(request):
    catalog_dict = {}
    main_categories = Category.objects.filter(categories_id__isnull=True)
    for cat in main_categories:
        catalog_dict[cat.title] = Category.objects.filter(categories_id=cat.id)

    return render(request, 'mainapp/catalog_main.html', {"dict": catalog_dict})


def contact(request):
    contact_data = {
        "Телефон": "+7-915-888-88-99",
        "e-mail": "example@mail.ru",
    }
    return render(request, 'mainapp/contact.html', {"dict": contact_data})


def catalog_category(request):
    category_name = request.path.split('/')[-2]

    cur_category = Category.objects.filter(translit_title=category_name)[0]
    nav_bar = [cur_category]

    while nav_bar[-1].categories:
        nav_bar.append(nav_bar[-1].categories)

    nav_bar.reverse()
    products = Product.objects.filter(category__translit_title=category_name)

    return render(request, 'mainapp/catalog.html', {"products": products, "nav_bar": nav_bar[1:]})


def sales(request):
    dict = {"1": "img/sale1.jpeg",
            "2": "img/sale2.jpeg",
            "3": "img/sale3.jpeg",
            "4": "img/sale4.jpg"}
    return render(request, 'mainapp/sales.html', {"dict": dict})


def item(request):

    prod_name = request.path.split('/')[-2]

    cur_prod = Product.objects.filter(translit_title=prod_name)[0]
    nav_bar = [cur_prod, cur_prod.category]

    while nav_bar[-1].categories:
        nav_bar.append(nav_bar[-1].categories)

    nav_bar.reverse()

    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "0.00",
        "item_name": cur_prod.title,
        "invoice": "unique-invoice-id",
        "notify_url": "https://www.example.com" + 'paypal-ipn'[::-1],
        "return_url": "https://www.example.com/your-return-location/",
        "cancel_return": "https://www.example.com/your-cancel-location/",
        "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'mainapp/item.html',
                  {"product": cur_prod, 'form': form, 'nav_bar': nav_bar[1:]})


def cart(request):

    _cart = get_or_create_cart(request, response=None, create=False)

    cart_products = []
    if _cart:
        cart_products = _cart.productcart_set.all()

    cart_products_ = list(cart_products)
    paypal_dict = {
        "cmd": "_cart",
        "upload": 1,
        "business": "receiver_email@example.com",
        # "amount_1": "159.00",
        # "item_name_1": "Перфоратор DeWALT D25103K",
        # "item_name_2": "Перфоратор DeWALT D25103K",
        # "amount_2": "178.00",
        "return_url": "https://127.0.0.1:8000/",
    }
    cart_products = []
    for i, pc in enumerate(cart_products_):
        cart_products.append([pc.quantity, pc.product])
        paypal_dict["amount_%d" % i] = pc.product.price * pc.quantity
        paypal_dict["item_name_%d" % i] = pc.product.title

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "cart_data": cart_products, 'cart': _cart}

    return render(request, 'mainapp/cart.html', context)


def add(request):
    response = HttpResponse("Добавлено")
    product = Product.objects.filter(id=int(request.GET['product_id']))[0]
    _cart = get_or_create_cart(request=request, response=response)

    product_cart = ProductCart.objects.filter(product=product, cart=_cart)

    if not product_cart:
        ProductCart(product=product, cart=_cart).save()
    else:
        product_cart[0].quantity += 1
        product_cart[0].save()

    _cart.save(_cache=True)

    return response


def remove(request):
    _cart = get_or_create_cart(request, response=None, create=False)
    prod = Product.objects.filter(id=int(request.GET['item']))[0]
    product_cart = ProductCart.objects.filter(product=prod, cart=_cart)
    if product_cart:
        product_cart[0].delete()

    _cart.save(_cache=True)
    return HttpResponse(str(_cart.total_price))


def page_not_found(request):
    return HttpResponse("Добавлено")


def get_total_price(request):
    _cart = get_or_create_cart(request)
    return HttpResponse('Сумма %s руб.' % str(_cart.total_price))
