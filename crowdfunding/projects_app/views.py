from django.shortcuts import render
from django.views import View
from .models import *
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView


# Create your views here.
class ProjectsView(View):
    def get(self, req, user_id):
        context = {'projects': Projects.objects.filter(id_user=user_id)}
        return render(req, 'projects/projects_list.html', context)

    def post(self, req):
        pass


class PicturesView(View):
    def get(self, req):
        pass

    def post(self, req):
        pass


class TagsView(View):
    def get(self, req):
        pass

    def post(self, req):
        pass


def addProject(req):
    context = {}
    context['categories'] = Category.objects.all()
    if (req.method == 'GET'):
        return render(req, 'projects/add_project.html', context)
    else:
        Projects.objects.create(id_user=1,title=req.POST['title'],total_target=req.POST['total_target'],
                                start=req.POST['start'],end=req.POST['end'],details=req.POST['details'],
                               category=Category.objects.get(id=req.POST['category']))
        return render(req, 'projects/add_project.html', context)