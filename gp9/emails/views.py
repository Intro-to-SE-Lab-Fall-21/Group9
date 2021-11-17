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
	to_remove = ""
	to_favorite = ""
	to_unfavorite = ""
	to_search = ""
	is_search = False
	removed = False
	if(request.GET.get('delete_email')):
		if(request.GET.get('email_delete')):
			to_remove = str(request.GET.get('email_delete'))
	if(request.GET.get('favorite_email')):
				if(request.GET.get('email_favorite')):
					to_favorite = str(request.GET.get('email_favorite'))
	if(request.GET.get('unfavorite_email')):
				if(request.GET.get('email_unfavorite')):
					to_unfavorite = str(request.GET.get('email_unfavorite'))
	if(request.GET.get('search_email')):
		to_search = str(request.GET.get('email_search'))
		is_search = True
	for filename in files:
		if to_remove == filename:
			os.remove(path+"/"+filename)
		else:
			with open(path+"/"+filename,'r') as f:
				lines = f.readlines()								
				with open(path+"/"+filename,'w') as fw:
					if to_favorite == filename:
							lines[9] = "Favorite: True\n"
					if to_unfavorite == filename:
						lines[9] = "Favorite: False\n"
					fw.writelines(lines)
				i = 0
				linesubj=""
				linefrom=""
				lineto=""
				linedate=""
				linemsg=""
				lineid = ""
				linefav = ""
				fav_to = False
				for line in lines:
					i = i+1
					#ignore
					if i <= 3 or i == 8 or i == 9:
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
					#date
					elif i == 7:
						linedate = line
					#message
					elif i == 10:
						linefav = line
						if "True" in line:
							fav_to = True
					else:
						if "-------------------------------------------------------------------------------" in line:
							pass
						else:
							linemsg += line
			if "to: "+username+"@gp9.com" in lineto.lower():
				if is_search:
					if to_search in linesubj or to_search in linefrom or to_search in lineto or to_search in linedate or to_search in linemsg:
						if fav_to:
							inbox.append({'subject': linesubj,'from':linefrom,'to':lineto,'date':linedate,'msg':linemsg,'id':filename,'favorite':linefav})
						else:			
							inbox.append({'subject': linesubj,'from':linefrom,'to':lineto,'date':linedate,'msg':linemsg,'id':filename})
				else:
					if fav_to:
						inbox.append({'subject': linesubj,'from':linefrom,'to':lineto,'date':linedate,'msg':linemsg,'id':filename,'favorite':linefav})
					else:			
						inbox.append({'subject': linesubj,'from':linefrom,'to':lineto,'date':linedate,'msg':linemsg,'id':filename})
	return render(request, "inbox.html", context={"inbox": inbox})