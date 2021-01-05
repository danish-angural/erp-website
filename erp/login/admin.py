from django.contrib import admin
from .models import User
from .models import Order
from .models import Details

admin.site.register(Order)
admin.site.register(User)
admin.site.register(Details)
