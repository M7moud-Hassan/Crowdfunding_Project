from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from  .views import *

urlpatterns = [
    path('add/',createProject,name="add_project"),
    path('project/<int:project_id>/',projectDetails,name="project_details"),
    path('project/<int:project_id>/comment', addComment, name='add_comment'),
    path('project/<int:project_id>/report', addReport, name='add_report'),
    path('project/<int:comment_id>/report_comment', addCommentReport, name='addCommentReport'),
    path('project/<int:project_id>/donate', addDonate, name='addDonate'),
    path('<int:project_id>/rate', rateProject, name='project_rate'),
    path('project/<int:comment_id>/reply', commentReply, name='comment_reply'),
]