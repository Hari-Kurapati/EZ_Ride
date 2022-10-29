"""adindia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from company_signup.views import signup_comp
from company_signin.views import company_signin
from company_signin.views import company_ads_list
from company_signin.views import delete_ad
from company_signin.views import add_stop
from user_signup.views import signup_user
from user_login.views import user_login
from purchase_list.views import user_purchase_list
from purchase_list.views import user_purchase_delete
from shop.views import shop
from shop.views import purchase_from_shop
from shop.views import not_available
from route.views import showroute,showmap

urlpatterns = [ 
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
    path('company_signup/', signup_comp, name="company_signup"),
    path('company_login/', company_signin, name="company_signin"),
    path('company_login/add_stop/', add_stop, name="add_stop"),
    path('user_signup/', signup_user, name="user_signup"),
    path('user_login/', user_login, name="user_login"),
    path('user_login/user_purchase_list/', user_purchase_list, name='user_purchase_list'),
    path('user_login/user_purchase_list/delete',user_purchase_delete, name='user_purchase_delete'),
    path('user_login/shop',shop, name='shop'),
    path('user_login/shop/purchase',purchase_from_shop,name='purchase_from_shop'),
    path('user_login/shop/not_available',not_available,name='not_available'),
    path('company_login/company_ads_list',company_ads_list,name='company_ads_list'),
    path('user_login/shop/company_ads_list/delete_ad',delete_ad,name='delete_ad'),
    path('<str:lat1>,<str:long1>,<str:lat2>,<str:long2>',showroute,name='showroute'),
    path('user_login/map',showmap,name='showmap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)