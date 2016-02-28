from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def main(request):
    return render(request, 'mainapp/main.html', {})


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
    dict = [[{"title":
                  "Бесщёточная компактная дрель/шуруповерт 13 мм XR Li-Ion, 14.4 В",
              "price": "2599 руб.",
              "img_url": "img/shurvert.jpg",
              "id": 1},
             {"title":
                  "Перфоратор DeWALT D25103K",
              "price": "8999 руб.",
              "img_url": "img/perf.jpg",
              "id": 2},
             {"title":
                  "Дисковая пила DeWalt DWE560",
              "price": "5599 руб.",
              "img_url": "img/pil.jpg",
              "id": 3}],
            [{"title":
                  "Двухскоростная дрель Makita DP4011",
              "price": "10990 руб.",
              "img_url": "img/5.jpg",
              "id": 4}]
            ]
    return render(request, 'mainapp/catalog.html', {"dict": dict})


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
            "price": "5599 руб."}

    return render(request, 'mainapp/item.html', {"dict": dict})


def cart(request):
    dict = [{"name": "Перфоратор DeWALT D25103K",
             "img_url": "img/perf.jpg",
             "number": "2",
             "price": str(8999 * 2),
             },
            {"name": "Перфоратор DeWALT D25103K",
             "img_url": "img/perf.jpg",
             "number": "2",
             "price": str(8999 * 2),
             },
            ]
    sum = 100500
    return render(request, 'mainapp/cart.html', {"dict": dict, "sum": sum})


def add(request):
    return HttpResponse("Добавлено")
