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
from django.conf.urls import include, url
from django.contrib.auth import views
import notifications.urls
from django.conf import settings
from django.conf.urls.static import static
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
    url(r'^approve_user/(?P<pk>\d+)/$', login_view.approve_user, name='approve_user'),
    url(r'^approve_order/(?P<pk>\d+)/$', login_view.approve_order, name='approve_order'),
    url(r'^change_order/(?P<pk>\d+)/$', login_view.change_order, name='change_order'),
    url(r'^view_details/(?P<pk>\d+)/$', login_view.view_details, name='view_details'),
    url(r'^download_customer_details/$', login_view.download_customer_details, name='download_customer_details'),
    url(r'^download_order_details/(?P<id>\d+)$', login_view.download_specific_order_details, name='download_specific_order_details'),
    url(r'^download_order_details/$', login_view.download_order_details, name='download_order_details'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
