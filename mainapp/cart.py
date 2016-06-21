from mainapp.models import Cart, create_customer
import random, string
from django.http import HttpResponse
from django.core.cache import cache
from mysite.settings import TIME

TOKEN_LEN = 40


def __generate_token(_len):
    """ Генерирует случайный токен для корзины """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(_len))


def get_or_create_cart(request, response=None, create=True):
    """
    Возвращает последнюю корзину пользователя или создает новую.
    Если необходимо добавляет token в response
    """
    if request.user.is_authenticated():
        if not request.user.customer:
            create_customer(request.user)

        cart = None
        cart = cache.get('cart_customer-' + str(request.user.customer.id))

        if not cart:
            try:
                cart = Cart.objects.filter(customer=request.user.customer, released=False).latest('date')
                cart = cache.set('cart_customer-' + str(request.user.customer.id),
                                 cart, TIME['HOUR'])
            except:
                cart = Cart(customer=request.user.customer)
                cart.save(_cache=True)
                pass

        return cart

    token = request.COOKIES.get('token', '')

    if token:
        cart = cache.get('cart_token-' + str(token))

        if cart and not cart.released:
            return cart
        elif cart:
            cart = Cart(token=token)

        if not cart:
            cart = Cart.objects.filter(token=token, released=False)

            if cart:
                cart = cart.latest('Data')
            else:
                cart = Cart(token=token)

            if cart.released:
                cart = Cart(token=token)

        cart.save(_cache=True)

        return cart

    if not create:
        return None

    token = __generate_token(TOKEN_LEN)
    cart = Cart(token=token)
    cart.save(_cache=True)

    response.set_cookie('token', token, TIME['MONTH'])

    return cart


def close_cart(_cart):
    """ Закрывает корзину после оплаты. Вполне может стать сложнее. """
    _cart.released = True
    _cart.save(_cache=True)
