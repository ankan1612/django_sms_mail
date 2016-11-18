from django.conf.urls import include, url
from django.contrib import admin
from sms import views as sms
from smsverification import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'django_sms_mail.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url
    (
        r'^$',
        views.send_sms_to,
        name='sms_verification'
    ),
    url
    (
        r'^smscode/',
        views.sms_verfication_code,
        name='sms_code'
    ),
]