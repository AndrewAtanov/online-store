from django.conf.urls import include, url
from django.contrib import admin
import socshop.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('mainapp.urls')),
    url(r'paypal/', include('paypal.standard.ipn.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('socshop.urls')),
]
