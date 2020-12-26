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
	if(user and user.utype=='PER'):
	 	return render(request,'superuser.html',{'user':user})
	'''
	if(user.utype=='SAL'):
		if(request.method=='GET'):
			data=Order.objects.all().filter(status='all approval pending')
			return render(request,'sales.html',{'user':user, 'data': data})
		else:
			pass
	'''		
	if(user.utype=='SUP'):
		if(request.method=='POST'):
			order=Order.objects.all().get(id=request.POST.get('id'))
			if(order.status == 'New draft'):
				order.status='New SO'
			order.save()
		data1=Order.objects.all().filter(status='New draft')
		data2=Order.objects.all().filter(status='Technical rejected SO')
		data3=Order.objects.all().filter(status='Finance rejected SO')
		return render(request,'support.html',{'user':user, 'data1': data1, 'data2':data2, 'data3':data3})


	if(user.utype=='OPE'):
		if(request.method=='POST'):
			order=Order.objects.all().get(id=request.POST.get('id'))
			if(order.status == 'New SO'):
				order.status='Technical approved SO'
			elif(order.status == 'Finance approval of SO'):
				order.status = 'Ready for dispatch'
			else:
				order.status = 'Dispatch completed'
			order.save()
		data1=Order.objects.all().filter(status='New SO')
		data2=Order.objects.all().filter(status='Finance approval of SO')
		data3=Order.objects.all().filter(status='Finance cleared for dispatch')
		return render(request,'operations.html',{'user':user, 'data1': data1, 'data2': data2, 'data3': data3})


	if(user.utype=='FIN'):
		if(request.method=='POST'):
			order=Order.objects.all().get(id=request.POST.get('id'))
			if(order.status == 'Technical approved SO'):
				order.status='Finance approval of SO'	
			elif(order.status == 'Ready for dispatch'):
				order.status = 'Finance cleared for dispatch'
			elif(order.status == 'Dispatch completed'):
				order.status = 'Final payments received'
			else:
				order.status = 'Order closed'
			order.save()
		data1=Order.objects.all().filter(status='Technical approved SO')
		data2=Order.objects.all().filter(status='Ready for dispatch')
		data3=Order.objects.all().filter(status='Dispatch completed')
		data4=Order.objects.all().filter(status='Final payments received')
		return render(request,'finance.html',{'user':user, 'data1': data1, 'data2': data2, 'data3': data3, 'data4':data4})
		
	
	if(user.utype=='SAL'):
		if(request.method=='GET'):
			form=OrderCreationForm()
			data=Order.objects.filter(sales=user.username)
			return render(request, 'sales.html',{'user':user, 'form':form, 'data': data})
		else:
			form=OrderCreationForm(request.POST)
			name = form.data.get('client')
			if(User.objects.filter(username=name).exists()):
				order=Order.objects.create(material=form.data.get('product'), quantity=form.data.get('quantity'), client=User.objects.get(username=name), sales=user.username, unit=form.data.get('unit'), unit_price=form.data.get('unit_price'), net_price=form.data.get('net_price'))
				order.save()
			form=OrderCreationForm()
			data=Order.objects.filter(sales=user.username)
			return render(request, 'sales.html',{'user':user, 'form':form, 'data': data})



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

def delete_order(request,pk):
	user = request.user
	query = Order.objects.get(pk=pk)
	if(user.utype == 'FIN'):
		query.status = 'Finance rejected SO'
		query.save()
	elif(user.utype == 'OPE'):
		query.status = 'Technical rejected SO'
		query.save()
	elif(user.utype == 'SUP'):
		query.delete()
	return redirect('home')

def change_order(request,pk):
	order = Order.objects.get(pk=pk)
	if(request.method == 'POST'):
		form = OrderCreationForm(request.POST)
		name = form.data.get('client')
		user = request.user
		sales = order.sales
		order.delete()
		order=Order.objects.create(material=form.data.get('product'), quantity=form.data.get('quantity'), client=User.objects.get(username=name), sales=sales, unit=form.data.get('unit'), unit_price=form.data.get('unit_price'), net_price=form.data.get('net_price'))
		order.save()
		return redirect('home')
	form = OrderCreationForm(initial={'product':order.material,'quantity':order.quantity, 'unit':order.unit, 'unit_price':order.unit_price, 'net_price':order.net_price, 'client':order.client.username})
	return render(request, 'change.html', {'form':form, 'data':order})