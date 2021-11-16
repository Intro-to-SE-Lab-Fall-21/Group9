from django.contrib.auth.backends import RemoteUserBackend
from django.shortcuts import  render, redirect
from .forms import ComposeMessage, NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.core.mail import BadHeaderError, send_mail, EmailMessage
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
				msg = EmailMessage(subject, message, sender, [recipient])
				try:
					file = form.cleaned_data['file']
					msg.attach(file)
				except:
					pass
				msg.send()
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			messages.success(request, 'Message sent.')
			return HttpResponseRedirect('/compose')
		else:
			return HttpResponse('Make sure all fields are entered and valid.')
	return render(request, 'compose.html', {'form': form})

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
	username = None
	inbox = []
	username = request.user.username
	path = f"{settings.MEDIA_ROOT}/email_out"
	files = os.listdir(path)
	for filename in files:
		with open(path+"/"+filename) as f:
			lines = f.readlines()
			i = 0
			linesubj=""
			linefrom=""
			lineto=""
			linedate=""
			linemsg=""
			for line in lines:
				i = i+1
				#ignore
				if i <= 3 or i == 8:
					pass
				#subject
				elif i == 4:
					linesubj = line
				#from
				elif i == 5:
					linefrom = line
				#to
				elif i == 6:
					lineto = line
					#if "To: "+username+"@gp9.com" in line:
						#inbox += [filename]
						#pass
				#date
				elif i == 7:
					linedate = line
				#message
				else:
					if "-------------------------------------------------------------------------------" in line:
						pass
					else:
						linemsg += line
			if "to: "+username+"@gp9.com" in lineto.lower():
				inbox.append({'subject': linesubj,'from':linefrom,'to':lineto,'date':linedate,'msg':linemsg})
	return render(request, "inbox.html", context={"inbox": inbox})