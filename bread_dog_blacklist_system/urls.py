"""bread_dog_blacklist_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import system.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', system.views.login),
    path('logout/', system.views.logout),
    path('user/', system.views.user),
    path('user/panel/', system.views.user),
    path('user/panel/content/', system.views.panel),
    path('user/all-bans/', system.views.user),
    path('user/all-bans/content/', system.views.all_bans),
    path('user/my-bans/', system.views.user),
    path('user/my-bans/content/', system.views.my_bans),
    path('user/add-ban/', system.views.user),
    path('user/add-ban/content/', system.views.add_ban),
    path('blacklist/', system.views.blacklist),
    path('copyright/', system.views.copyright),
    path('user/info/', system.views.get_info)
]
