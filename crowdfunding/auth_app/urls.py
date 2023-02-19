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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.db import models
from django.conf import settings
from django.conf.urls.static import static
from . import views
# from django.contrib.auth import views

urlpatterns = [
                  path('register', views.register, name='register'),
                  path('login', views.login, name='login'),
                  path('verify/<int:user_id>/', views.verify_email, name='verify_email'),
                  path('profile', views.profile, name='profile'),
                  path('editProfile', views.editProfile, name='edit_profile'),
                  path('deleteAccount', views.deleteAccount, name='deleteAccount'),
                  path('delete/<int:user_id>',views.confirmDeleteAccount,name='delete_account'),
                  path('logout',views.logout,name='logout'),
                  path('resetpassword',views.resetPassword,name='resetpassword'),
                  path('setpassword/<str:email>', views.sendEmailPassword, name='setpassword'),
                  path('facelogin',views.facelogin, name='facelogin' ),
                  path('facelogout',views.facelogin, name='facelogout' ),
                  path('social-auth/', include('social_django.urls',namespace='social')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
