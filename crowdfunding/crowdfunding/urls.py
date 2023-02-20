"""crowdfunding URL Configuration

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
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('blog/', includes('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from projects_app import  urls as projcets_urls
from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls.static import static
from django.conf import settings
from home_page_app import urls as home_page
from auth_app import urls as auth_url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include(projcets_urls)),
    path('homePage/',include(home_page)),
    path('',include(auth_url))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
