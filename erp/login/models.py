from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	utype = models.CharField(max_length = 3, default = 'CUS', editable = True)
	approved = models.CharField(max_length=3, default='NO', editable=True)

class Order(models.Model):
	status=models.CharField(default='New draft', max_length=100)
	material=models.CharField(max_length=20)
	quantity=models.IntegerField()
	unit=models.CharField(max_length=10,default='m')
	unit_price = models.IntegerField(default=0)
	net_price = models.IntegerField(default=0)
	date=models.DateTimeField(auto_now=True, editable=True)
	client=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	sales = models.CharField(max_length=100, default='no sales')
	optfield1=models.CharField(blank=True, max_length=100)
	optfield2=models.CharField(blank=True, max_length=100)
	optfield3=models.CharField(blank=True, max_length=100)
	optfield4=models.CharField(blank=True, max_length=100)

class Details(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	date = models.DateTimeField(auto_now=True)
	status=models.CharField(default='New draft', max_length=100)