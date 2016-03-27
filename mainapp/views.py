from django.shortcuts import render
from django.http import HttpResponse
from paypal.standard.forms import PayPalPaymentsForm
from .models import Product

# Create your views here.

cart_ids = []


def main(request):
    context = {}
    context["auth"] = True
    if not request.user.is_authenticated():
        context["auth"] = False
    return render(request, 'mainapp/main.html', context)


def catalog(request):
    catalog_dict = {"Инструменты":
                        ["1", "2", "3", "4"],
                    "Электроинструменты":
                        ["1", "2", "4"],
                    "Стройматериалы":
                        ["1", "2", "3", "4"],
                    "Что-то еще":
                        ["1", "2", "3"],
                    "Ну и на последок":
                        ["Чтобы", "Футер", "Не", "Лез", "Вверх"]
                    }
    return render(request, 'mainapp/catalog_main.html', {"dict": catalog_dict})


def contact(request):
    contact_data = {
        "Телефон": "+7-915-888-88-99",
        "e-mail": "example@mail.ru",
    }
    return render(request, 'mainapp/contact.html', {"dict": contact_data})


def catalog_category(request):
    products = Product.objects.all()

    return render(request, 'mainapp/catalog.html', {"products": products})


def sales(request):
    dict = {"1": "img/sale1.jpeg",
            "2": "img/sale2.jpeg",
            "3": "img/sale3.jpeg",
            "4": "img/sale4.jpg"}
    return render(request, 'mainapp/sales.html', {"dict": dict})


def item(request):
    dict = {"item_name": "Перфоратор DeWALT D25103K",
            "description": "Мощная 18.0 В XR Li-Ion компактная дрель/шуруповерт последнего поколения с новыми уникальными аккумуляторами 5,0 Ач технологии XR Li-Ion Технология бесщёточных двигателей Brushless для превосходной эффективности и производительности инструмента Очень компактный, лёгкий и эргономичный дизайн, позволяющий использовать инструмент в ограниченном пространстве",
            "prop": {"prop1": "val1", "prop2": "val2", "prop3": "val3"},
            "main_feature": ["main feature 1", "main feature 2", "main feature 3"],
            "price": "5599 руб."
            }

    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "0.00",
        "item_name": dict['item_name'],
        "invoice": "unique-invoice-id",
        "notify_url": "https://www.example.com" + 'paypal-ipn'[::-1],
        "return_url": "https://www.example.com/your-return-location/",
        "cancel_return": "https://www.example.com/your-cancel-location/",
        "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'mainapp/item.html', {"dict": dict, 'form': form})


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
    cart_ids.append(int(request.GET['item']))
    return HttpResponse("Добавлено")


def page_not_found(request):
    return HttpResponse("Добавлено")
