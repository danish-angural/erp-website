from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES=(
        (1, 'sales staff'),
        (2, 'sales admin'),
        (3, 'operations admin'),
        (4, 'finance admin'),
    )

