from django.shortcuts import render
from sms.utils import send_twilio_message
from sms.utils import verification_code_generator
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from smsverification.forms import SMSVerificationForm
from smsverification.forms import SMSCodeFrom
import re


def send_sms_to(request):
    if 'code' in request.session:
        try:
            del request.session['code']
        except Exception:
            pass
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SMSVerificationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            number = form.cleaned_data['Phone_Number']
            code = verification_code_generator()
            body='Your 4 digit veification code is : ' + code
            # call twilio
            sent,status = send_twilio_message(number, body)
            if status==True:
                form2 = SMSCodeFrom()
                request.session['code'] = code
                return HttpResponseRedirect(reverse('sms_code'))
            else:
                s=str(sent)[str(sent).rfind('Twilio returned the following information:'):str(sent).rfind('More information may be available here:')]
                s=s[:s.rfind('.')+1]
                pattern = re.compile("[A-Z]")
                st=''
                m = pattern.search(s, s.find(':')) 
                s = s[:s.find(':')+1] + '\n' + s[m.start():]
                return render(request, 'smsverification/index.html', {'form': form, 'error': str(s)})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SMSVerificationForm()
    return render(request, 'smsverification/index.html', {'form': form})
    
    
def sms_verfication_code(request):
    if 'code' not in request.session:
        return HttpResponseRedirect(reverse('sms_verification'))
    if request.method == 'POST':
        form = SMSCodeFrom(request.POST)
        if form.is_valid():
            code = form.cleaned_data['Code']
            if code==request.session['code']:
                try:
                    del request.session['code']
                except Exception:
                    pass
                return render(request, 'smsverification/code.html', {'form': form, 'success': "Successfully verified your phone number"})
            else:
                return render(request, 'smsverification/code.html', {'form': form, 'error': "Verification failed! Try Again"})
        else:
            return render(request, 'smsverification/code.html', {'form': form})
    else:
        form = SMSCodeFrom()
        return render(request, 'smsverification/code.html', {'form': form})
    
