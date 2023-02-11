from django.shortcuts import render
from django.views import View
from .models import *
from django.views.generic import ListView

# Create your views here.


class CategoryView(View):
    def get(self,req):
        pass
    def post(self,req):
        def add_items(req):
            item = Category(data=req.data)

            # validating for already existing data
            if Category.objects.filter(**req.data).exists():
                raise Category.ValidationError('This data already exists')

            if item.is_valid():
                item.save()
                return Response(item.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)


class ProjectsView(View):
    def get(self,req):
        pass
    def post(self,req):
        pass



class PicturesView(View):
    def get(self,req):
        pass
    def post(self,req):
        pass


class TagsView(View):
    def get(self,req):
        pass
    def post(self,req):
        pass