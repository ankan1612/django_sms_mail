from django.shortcuts import render
from sms.forms import SendSMSForm
from sms.utils import send_twilio_message
from django.conf import settings
from datetime import datetime
from decimal import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import re


def send_sms_to(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SendSMSForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            number = form.cleaned_data['to_number']
            body = form.cleaned_data['body']
            # call twilio
            sent,status = send_twilio_message(number, body)
            if status==True:
                # save form
                send_sms = form.save(commit=False)
                send_sms.to_number = number
                send_sms.body = body
                send_sms.from_number = settings.TWILIO_PHONE_NUMBER
                send_sms.sms_sid = sent.sid
                send_sms.account_sid = sent.account_sid
                send_sms.status = sent.status
                send_sms.sent_at = datetime.now()
                send_sms.save()
                # redirect to a new URL:
                return render(request, 'sms/sms.html', {'form': form, 'success': number})
            else:
                s=str(sent)[str(sent).rfind('Twilio returned the following information:'):str(sent).rfind('More information may be available here:')]
                s=s[:s.rfind('.')+1]
                pattern = re.compile("[A-Z]")
                st=''
                m = pattern.search(s, s.find(':')) 
                s = s[:s.find(':')+1] + '\n' + s[m.start():]
                return render(request, 'sms/sms.html', {'form': form, 'error': str(s)})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SendSMSForm()
    return render(request, 'sms/sms.html', {'form': form})