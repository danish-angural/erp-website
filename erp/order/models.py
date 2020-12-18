from django.db import models
import os
import  sys
sys.path.append(os.path.realpath('.'))
from login.models import User
class Order(models.Model):
    material=models.CharField(max_length=20)
    quantity=models.IntegerField()
    date=models.DateTimeField(auto_created=True)
    client=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
