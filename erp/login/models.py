from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	utype = models.CharField(max_length = 3, default = 'CUS', editable = True)


