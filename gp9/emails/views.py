from django.contrib.auth.backends import RemoteUserBackend
from django.shortcuts import  render, redirect
from .forms import ComposeMessage, NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.conf import settings
def compose(request):
	username = request.user.username
	if request.method == 'GET':
		form = ComposeMessage()
	if request.method == "POST":
		form = ComposeMessage(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			recipient = form.cleaned_data['recipient']
			sender = str(username)+'@gp9.com'
			try:
				send_mail(subject, message, sender, [recipient])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			#return HttpResponse('Sent.')
			messages.success(request, 'Message sent.')
			return HttpResponseRedirect('compose')
		else:
			return HttpResponse('Make sure all fields are entered and valid.')
	return render(request, 'compose.html', {'form': form})
    #subject = request.POST.get('subject', '')
    #message = request.POST.get('message', '')
    #to_email = request.POST.get('to_email', '')

def homepage(request):
	return render(request=request, template_name='homepage.html')

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("emails:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("emails:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("emails:homepage")

def inbox(request):

    path = f"{settings.MEDIA_ROOT}/email_out"
    inbox = os.listdir(path)

    return render(request, "inbox.html", context={"inbox": inbox})