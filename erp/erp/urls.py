"""erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views as login_view
from django.conf.urls import url
from django.contrib.auth import views

admin.site.index_template = 'admin/my_index.html'
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view.main, name='main'),
    path('home/', login_view.home, name='home'),
    path('signup/', login_view.signup, name='signup'),
    path('login/', login_view.user_login, name='login'),
    path('logout/', login_view.user_logout, name='logout'),
    url(r'^delete_order/(?P<pk>\d+)/$', login_view.delete_order, name='delete_order'),
]
