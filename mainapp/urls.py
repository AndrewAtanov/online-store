from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^catalog$', views.catalog, name='catalog'),
    url(r'^contact$', views.contact, name='contact')
]
