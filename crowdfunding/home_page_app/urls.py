
from django.urls import path
from .views import *
from  .views import *

urlpatterns = [
    path('', home, name='home_page'),
    path('my_projects', getAllMyProjects, name='getAllMyProjects'),
    path('', home, name='home_page'),
    path('my_projects', getAllMyProjects, name='getAllMyProjects')

]