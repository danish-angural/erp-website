from django.contrib.auth import logout, login, authenticate,forms
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, OrderCreationForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
#from django.contrib.auth.models import User
from django.urls import reverse
from . models import User, Order, Details
from notifications.signals import notify
# Create your views here.
from datetime import date, time
def main(request):
    return render(request, 'main.html',{})

def home(request):
	user=request.user
	num = {}
	num['New draft'] =  Order.objects.filter(status='New draft').count()
	num['New SO'] =  Order.objects.filter(status='New SO').count()
	num['Technical approved SO'] =  Order.objects.filter(status='Technical approved SO').count()
	num['Finance approval of SO'] =  Order.objects.filter(status='Finance approval of SO').count()
	num['Ready for dispatch'] =  Order.objects.filter(status='Ready for dispatch').count()
	num['Finance cleared for dispatch'] =  Order.objects.filter(status='Finance cleared for dispatch').count()
	num['Dispatch completed'] =  Order.objects.filter(status='Dispatch completed').count()
	num['Final payments received'] =  Order.objects.filter(status='Final payments received').count()
	num['Technical rejected SO'] =  Order.objects.filter(status='Technical rejected SO').count()
	num['New draft'] =  Order.objects.filter(status='Finance rejected SO').count()
	if(user and user.utype=='PER'):
	 	return render(request,'superuser.html',{'user':user, 'notifications':request.user.notifications.all()})
	if(user.utype=='SUP'):
		data1=Order.objects.all().filter(status='New draft')
		data2=Order.objects.all().filter(status='Technical rejected SO')
		data3=Order.objects.all().filter(status='Finance rejected SO')
		return render(request,'support.html',{'user':user, 'data1': data1, 'data2':data2, 'data3':data3, 'num':num, 'notifications':request.user.notifications.all()})


	if(user.utype=='OPE'):
		data1=Order.objects.all().filter(status='New SO')
		data2=Order.objects.all().filter(status='Finance approval of SO')
		data3=Order.objects.all().filter(status='Finance cleared for dispatch')
		return render(request,'operations.html',{'user':user, 'data1': data1, 'data2': data2, 'data3': data3, 'num':num, 'notifications':request.user.notifications.all()})


	if(user.utype=='FIN'):
		data1=Order.objects.all().filter(status='Technical approved SO')
		data2=Order.objects.all().filter(status='Ready for dispatch')
		data3=Order.objects.all().filter(status='Dispatch completed')
		data4=Order.objects.all().filter(status='Final payments received')
		data5=User.objects.all().filter(approved='NO')
		return render(request,'finance.html',{'user':user, 'data1': data1, 'data2': data2, 'data3': data3, 'data4':data4, 'data5': data5, 'num':num, 'notifications':request.user.notifications.all()})
		
	
	if(user.utype=='SAL'):
		if(request.method=='GET'):
			form=OrderCreationForm()
			data=Order.objects.filter(sales=user.username)
			return render(request, 'sales.html',{'user':user, 'form':form, 'data': data, 'notifications':request.user.notifications.all()})
		else:
			form=OrderCreationForm(request.POST)
			name = form.data.get('client')
			if(User.objects.filter(username=name).exists()):
				order=Order.objects.create(material=form.data.get('product'), quantity=form.data.get('quantity'), client=User.objects.get(username=name), sales=user.username, unit=form.data.get('unit'), unit_price=form.data.get('unit_price'), net_price=form.data.get('net_price'))
				order.save()
				notify.send(sender=request.user, recipient=User.objects.all().filter(approved='Yes'), verb=user.username+' approved '+order.material+' on ' +date.today().strftime("%B %d, %Y")+ ' to status '+order.status)
			form=OrderCreationForm()
			data=Order.objects.filter(sales=user.username)
			return render(request, 'sales.html',{'user':user, 'form':form, 'data': data, 'notifications':request.user.notifications.all()})



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
		for each in User.objects.all():
				Notifications.objects.create(order=query,user=user, recipient=each.id)
	elif(user.utype == 'OPE'):
		query.status = 'Technical rejected SO'
		query.save()
		for each in User.objects.all():
				Notifications.objects.create(order=query,user=user, recipient=each.id)
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

def notify_delete(request,pk):
	query = Notifications.objects.get(pk=pk)
	query.delete()
	return redirect('home')

def approve_user(request,pk):
	user = User.objects.get(pk=pk)
	user.approved = 'Yes'
	user.save()
	return redirect('home')

def approve_order(request,pk):
	order = Order.objects.get(pk=pk)
	user = request.user
	if(order.status == 'New draft' and user.utype == 'SUP'):
		order.status='New SO'
	elif(order.status == 'New SO' and user.utype == 'OPE'):
		order.status='Technical approved SO'
	elif(order.status == 'Technical approved SO' and user.utype == 'FIN'):
		order.status = 'Finance approval of SO'
	elif(order.status == 'Finance approval of SO' and user.utype == 'OPE'):
		order.status='Ready for dispatch'
	elif(order.status == 'Ready for dispatch' and user.utype == 'FIN'):
		order.status = 'Finance cleared for dispatch'
	elif(order.status == 'Finance cleared for dispatch' and user.utype == 'OPE'):
		order.status='Dispatch completed'
	elif(order.status == 'Dispatch completed' and user.utype == 'FIN'):
		order.status = 'Final payments received'
	elif(order.status == 'Final payments received' and user.utype == 'FIN'):
		order.status='Order closed'
	order.save()
	notify.send(sender=request.user, recipient=User.objects.all().filter(approved='Yes'), verb=user.username+' approved '+order.material+' on ' +date.today().strftime("%B %d, %Y")+ ' to status '+order.status)
	detail = Details.objects.create(order=order, status=order.status)
	detail.save()
	return redirect('home')

def view_details(request,pk):
	order = Order.objects.get(pk=pk)
	details = Details.objects.filter(order=order)
	return render(request,'view_details.html',{'details':details, 'order':order})