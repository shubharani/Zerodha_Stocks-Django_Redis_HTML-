"""zerodha URL Configuration

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
from django.urls import path , include
from rest_framework.urlpatterns import format_suffix_patterns
from vue_app.views import home

from vue_app import views as vue_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # path('t1',vue_views.test_vue),
    path('t2', vue_views.home, name='home'),
    # path('', manage_items, name="items"),
    # path('<slug:key>', manage_item, name="single_item")
]

urlpatterns = format_suffix_patterns(urlpatterns)