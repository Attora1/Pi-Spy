from django.shortcuts import render
from twilio.rest import Client
from django.conf import settings
from twilio.twiml.messaging_response import MessagingResponse
from django_twilio.decorators import twilio_view

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Function to send package arrival message
# At the moment you can activate by going to a web page
# But this should be changed to whenever a package is detected
def sendArrivalMessage(request):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = "A new package has been detected at your doorway. Please check the website for more info."
    to = "+13137199896"
    num_from = "+19478004230"
    response = client.messages.create(body=message, to=to, from_=num_from)

    return render(request, 'index.html')

# Function to send package removal message
# At the moment you can activate by going to a web page
# But this should be changed to whenever a package is removed
def sendRemovalMessage(request):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = "The package has been retrieved. If you were not the one who picked up the package, browse to your local Pi-Spy for more details."
    to = "+13137199896"
    num_from = "+19478004230"
    response = client.messages.create(body=message, to=to, from_=num_from)

    return render(request, 'index.html')
    
# Sends a message when a user replies to the Automated message
# Needs work for reading user's reply
@twilio_view
def reply_to_sms_messages(request):
    # Start our TwiML response
    resp = MessagingResponse()

    resp.message("")

    return resp