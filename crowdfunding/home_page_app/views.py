from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from projects_app.models import Project, Donation, Category, Tag
from django.db.models import Avg
from django.http import HttpResponseRedirect



def categoryProjects(request, cat_id):
    try:
        cat=Category.objects.filter(id=cat_id)
        if cat:
            projects = Project.objects.filter(
                category_id=cat_id).all()
            images = []
            for project in projects:
                images.append(project.image_set.all().first().images.url)
            context = {
                    'show':'show project by category '+Category.objects.get(id=cat_id).name,
                    'projects': projects,
                    'images': images,
                    'categories': Category.objects.all(),
            }
            return render(request, "home/show_categories.html", context)
        else:
            return HttpResponseRedirect('/homePage')
    except:
        return HttpResponseRedirect('/homePage')
def search(request):
    try:
        search_post = request.POST['search']
        if search_post:
            projects = Project.objects.filter(title__icontains=search_post)
            searched_tags = Tag.objects.filter(name__icontains=search_post)
            images = []
            for project in projects:
               images.append(project.image_set.all().first().images.url)
            context = {
                'projects': projects,
                'tags': searched_tags,
                'images': images,
                'show': 'search about '+search_post,
                'categories': Category.objects.all(),
                }
            return render(request, "home/show_categories.html", context)
        else:
            return HttpResponseRedirect('/homePage')
    except:
        return HttpResponseRedirect('/homePage')
def tagProjects(request, tag_id):
    try:
        tag = Tag.objects.filter(id=tag_id)
        if tag:
            projects = tag[0].project_set.all()
            images = []
            for project in projects:
                images.append(project.image_set.all().first().images.url)

            context = {
                'projects': projects,
                'images': images,
                'show':'show project by tag '+tag[0].name,
                'categories': Category.objects.all(),
            }
            return render(request, "home/show_categories.html", context)
        else:
            return HttpResponseRedirect('/homePage')
    except:
        return HttpResponseRedirect('/homePage')