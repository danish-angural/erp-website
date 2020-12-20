from django.contrib import admin
from .models import User
from .models import Order

admin.site.register(Order)
admin.site.register(User)
