from django.shortcuts import redirect
from django.shortcuts import render
from twilio.rest import Client
from django.conf import settings
from twilio.twiml.messaging_response import MessagingResponse
from django_twilio.decorators import twilio_view

# Create your views here.
def index(request):
	return render(request, "index.html")

def camView(request):
	return render(request, "cam.html")

def profile(request):
	return render(request, "gallery.html")

def settings(request):
	return render(request, "settings.html")

def contact(request):
	return render(request, "contact.html")

def log(request):
	return render(request,"camlog.html")

def gallery(request):

	return render(request, "profile.html")

@twilio_view
def replyToMessage(request):
	body = str(request.POST['Body'])
	resp = MessagingResponse()
	
	if body.lower() == "no":
		resp.message("Thank you for responding. It is recommended to check the log files and contact the authorities.")

	elif body.lower() == "yes":
		resp.message("Thank you for responding.")
	
	return resp

