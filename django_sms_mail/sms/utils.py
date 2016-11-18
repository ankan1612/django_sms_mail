from django.conf import settings
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
import string
import random
import twilio
 
 
def send_twilio_message(to_number, body):
    client = TwilioRestClient(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
 
    try:
        return client.messages.create(body=body,
                    to=to_number,    # Replace with your phone number
                    from_=settings.TWILIO_PHONE_NUMBER), True # Replace with your Twilio number
    except TwilioRestException as e:
        return e, False
        

def verification_code_generator():
    choose_from = string.digits+string.ascii_uppercase+string.ascii_lowercase
    return ''.join(random.choice(choose_from) for x in range(4))
    