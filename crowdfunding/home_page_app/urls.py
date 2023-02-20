
from django.urls import path
from  .views import *

urlpatterns = [
    path('',home,name='home_page'),
    path('category/<int:cat_id>',categoryProjects,name='getCategories'),
    path('search/', search, name='search'),
    path('tags_projects/<int:tag_id>', tagProjects, name='getProjectTags'),
    path('my_projects',getAllMyProjects,name='getAllMyProjects')
]