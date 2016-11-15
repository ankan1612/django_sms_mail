from django.contrib import admin

# Register your models here.
from sms.models import SendSMS

admin.site.register(SendSMS)