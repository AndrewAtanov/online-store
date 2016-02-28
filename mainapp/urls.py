from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^catalog/$', views.catalog, name='catalog'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^catalog/[a-z]+/$', views.catalog_category, name="catalog category"),
    url(r'^sales$', views.sales, name="sales"),
    url(r'^catalog/[a-z]+/[a-z]+/$', views.item, name="item"),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^add-to-cart/$', views.add, name='add'),
]
