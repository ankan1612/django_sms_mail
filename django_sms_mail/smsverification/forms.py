from django import forms

class SMSVerificationForm(forms.Form):
    Phone_Number = forms.CharField(label='Phone Number', max_length=15, required=True)
    
    
class SMSCodeFrom(forms.Form):
    Code = forms.CharField(label='Verification Code', max_length=4, required=True)