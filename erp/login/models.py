from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	utype = models.CharField(max_length = 3, default = 'CUS', editable = True)

class Order(models.Model):
	status=models.CharField(default='all approval pending', max_length=100)
	material=models.CharField(max_length=20)
	quantity=models.IntegerField()
	date=models.DateTimeField(auto_now=True)
	client=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
