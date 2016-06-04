from django.shortcuts import render
from django.http import HttpResponse
from paypal.standard.forms import PayPalPaymentsForm
from .models import Product, Category, Cart
import  string, random
from datetime import datetime

random.seed(datetime.now())

# Create your views here.

cart_ids = set()
TOKEN_LEN = 40
ONE_MONTH = 24 * 60 * 60 * 31

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


def __generate_token(_len):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(_len))


def cart(request):

    cart_data = Product.objects.filter(id__in=cart_ids)
    cost_sum = 0
    for _item in cart_data:
        cost_sum += _item.price



    # What you want the button to do.
    paypal_dict = {
        "cmd": "_cart",
        "upload": 1,
        "business": "receiver_email@example.com",
        "amount_1": "159.00",
        "item_name_1": "Перфоратор DeWALT D25103K",
        "item_name_2": "Перфоратор DeWALT D25103K",
        "amount_2": "178.00",
        # "invoice": "unique-invoice-id",
        # "notify_url": "https://www.example.com" + 'paypal-ipn'[::-1],
        "return_url": "https://127.0.0.1:8000/",
        # "cancel_return": "https://www.example.com/your-cancel-location/",
        # "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "cart_data": cart_data, "cost_sum": cost_sum}

    return render(request, 'mainapp/cart.html', context)


def add(request):
    token = request.session._session.get('token', '')
    add_token = False
    if not token:
        token = __generate_token(TOKEN_LEN)
        _c = Cart(token=token)
        _c.save()
        add_token = True

    cur_cart = Cart.objects.filter(token=token)[0]
    cur_cart.products.add(Product.objects.filter(id=int(request.GET['product_id']))[0])

    response = HttpResponse("Добавлено")

    if add_token:
        response.set_cookie('token', token, ONE_MONTH)

    return response


def remove(request):
    cart_ids.remove(int(request.GET['item']))
    return HttpResponse(cart_ids.__str__())


def page_not_found(request):
    return HttpResponse("Добавлено")
