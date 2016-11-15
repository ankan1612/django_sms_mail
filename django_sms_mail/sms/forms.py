from django import forms
from sms.models import SendSMS
from django.forms import ModelForm, Textarea

class SendSMSForm(forms.ModelForm):
 
    def __init__(self, *args, **kwargs):
        super(SendSMSForm, self).__init__(*args, **kwargs)
        self.fields['to_number'].required = True
        self.fields['to_number'].widget.attrs.update({'class' : 'input-xlarge'})
        self.fields['body'].widget.attrs.update({'class' : 'input-xlarge'})
        

    class Meta:
        model = SendSMS
        fields = ('to_number', 'body')
        widgets = {
            'body': Textarea(attrs={'cols': 70, 'rows': 4}),
        }