from django.contrib.auth import logout, login, authenticate,forms
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
#from django.contrib.auth.models import User
from django.urls import reverse
from . import models

# Create your views here.
def main(request):
    return render(request, 'main.html',{})

def home(request):
	return render(request,'home.html',{})

def signup(request):
	if(request.method=='POST'):
		print('$')
		form = CustomUserCreationForm(request.POST)
		print('$')
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			firstname = form.cleaned_data.get('firstname')
			lastname = form.cleaned_data.get('lastname')
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			print('$')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
		else:
			print('&')
			messages.error(request, "Error")
	else:
		print('^')
		form = CustomUserCreationForm()
	return render(request, 'signup.html', {'form': form})