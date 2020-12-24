from django.contrib.auth import logout, login, authenticate,forms
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, OrderCreationForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
#from django.contrib.auth.models import User
from django.urls import reverse
from . import models
from . models import User, Order
# Create your views here.
def main(request):
    return render(request, 'main.html',{})

def home(request):
	user=request.user
	# if(user and user.utype=='PER'):
	# 	return render(request,'superuser.html',{'user':user})
	if(user.utype=='SAL'):
		if(request.method=='GET'):
			data=Order.objects.all().filter(status='all approval pending')
			return render(request,'sales.html',{'user':user, 'data': data})
		else:
			pass
			


	if(user.utype=='SUP'):
		if(request.method=='GET'):
			data=Order.objects.all().filter(status='sales approval pending')
			return render(request,'sales.html',{'user':user, 'data': data})
		else:
			pass


	if(user.utype=='OPE'):
		if(request.method=='GET'):
			data=Order.objects.all().filter(status='operations approval pending')
			return render(request,'operations.html',{'user':user, 'data': data})
		else:
			order=Order.objects.all().get(id=request.POST.get('id'))
			order.status='finance approval pending'
			order.save()
			data=Order.objects.all().filter(status='operations approval pending')
			return render(request,'operations.html',{'user':user, 'data': data})


	if(user.utype=='FIN'):
		if(request.method=='GET'):
			data=Order.objects.all().filter(status='finance approval pending')
			return render(request,'operations.html',{'user':user, 'data': data})
		else:
			order=Order.objects.all().get(id=request.POST.get('id'))
			order.status='all approved'
			order.save()
			data=Order.objects.all().filter(status='finance approval pending')
			return render(request,'finance.html',{'user':user, 'data': data})
		
	
	if(user.utype=='CUS'):
		if(request.method=='GET'):
			form=OrderCreationForm()
			data=request.user.order_set.all()
			print(data)
			return render(request, 'customer.html',{'user':user, 'form':form, 'data': data})
		else:
			form=OrderCreationForm(request.POST)
			order=Order.objects.create(material=form.data.get('product'), quantity=form.data.get('quantity'), client=user)
			order.save()
			form=OrderCreationForm()
			data=request.user.order_set.all()
			print(data)
			return render(request, 'customer.html',{'user':user, 'form':form, 'data': data})



def signup(request):
	if(request.method=='POST'):
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			firstname = form.cleaned_data.get('firstname')
			lastname = form.cleaned_data.get('lastname')
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			print(user)
			return redirect('home')
	else:
		print(request.user)
		if(not request.user.is_anonymous):
			return redirect('/home/')
		form = CustomUserCreationForm()
		return render(request, 'signup.html', {'form': form})

def user_login(request):
	if(request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('home')
		else:
			return HttpResponse('invalid credentials')
	return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')