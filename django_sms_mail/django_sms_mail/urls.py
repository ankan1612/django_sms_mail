from django.conf.urls import include, url
from django.contrib import admin
from sms import views as sms
import smsverification


urlpatterns = [
    # Examples:
    # url(r'^$', 'django_sms_mail.views.home', name='home'),
    #  url(r'^blog/', include('blog.urls')),
    url(r'^smsverification/', include('smsverification.urls')),
   
    url(r'^admin/', include(admin.site.urls)),
    url
    (
        r'^$',
        sms.send_sms_to,
        name='send_sms'
    ),
    
]
