from mainapp.models import Cart, create_customer
import random, string
from django.http import HttpResponse

TOKEN_LEN = 40
ONE_MONTH = 24 * 60 * 60 * 31


def __generate_token(_len):
    """ Генерирует случайный токен для корзины """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(_len))


def get_or_create_cart(request, response, create=True):
    """
    Возвращает последнюю корзину пользователя или создает новую.
    Если необходимо добавляет token в response
    """
    if request.user.is_authenticated():
        if not request.user.customer:
            create_customer(request.user)

        try:
            cart = Cart.objects.filter(customer=request.user.customer, released=False).latest('date')
        except:
            cart = Cart(customer=request.user.customer)
            cart.save()

        return cart

    token = request.COOKIES.get('token', '')

    if token:
        return Cart.objects.filter(token=token).latest('date')

    if not create:
        return None

    token = __generate_token(TOKEN_LEN)
    cart = Cart(token=token)
    cart.save()

    response.set_cookie('token', token, ONE_MONTH)

    return cart
