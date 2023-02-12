from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from  .views import *

urlpatterns = [
    path('List/<int:user_id>',ProjectsView.as_view(),name='list_projects'),
    path('add/',addProject,name="add_project")
]