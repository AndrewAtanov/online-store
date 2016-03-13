from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm


def home(request):
    """
    Home page with auth links.
    """
    if request.user.is_authenticated():
        return HttpResponse("{0} <a href='/accounts/logout'>exit</a>".format(request.user))
    else:
        return HttpResponse("<a href='/login/vk-oauth2/'>login with VK</a>")


@login_required
def account_profile(request):
    """
    Show user greetings. Only for logged in users.
    """
    return HttpResponse("Hi, {0}! Nice to meet you.".format(request.user.first_name))


def account_logout(request):
    """
    Logout and redirect to the main page.
    """
    logout(request)
    return redirect('/')


@csrf_exempt
def paypal_success(request):
    """
    Tell user we got the payment.
    """
    return HttpResponse("Money is mine. Thanks.")


#@login_required
def paypal_pay(request):
    """
    Page where we ask user to pay with paypal.
    """
    paypal_dict = {
        "business": "acccko-facilitator@gmail.com",
        "amount": "100.00",
        "currency_code": "RUB",
        "item_name": "products in socshop",

        "invoice": "INV-00002",
        "notify_url": reverse('paypal-ipn'),
        "return_url": "http://localhost:8000/payment/success/",
        "cancel_return": "http://localhost:8000/payment/cart/",
        "custom": str(request.user.id)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "paypal_dict": paypal_dict}
    return render(request, "socshop/payment.html", context)
