from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from auth_app.models import RegisterUser
from projects_app.models import Project, Donation, Category, Tag
from django.db.models import Avg
from django.http import HttpResponseRedirect


# Create your views here.
@require_http_methods(["GET"])
def home(request):
    if 'user_id' in request.session:
        try:
            last_hightest_rate_projects = Project.objects.annotate(avg_rate=Avg('rate__rate')).order_by('avg_rate')[:5]
            images = []
            for p in last_hightest_rate_projects:
                images.append(p.image_set.all().first().images.url)
            last_5_projects = Project.objects.all()[:5]
            last_5_featured_projects = Project.objects.filter(is_featured=True).order_by('id')[:5]
            return render(request, 'home/home_page.html', context={
                'projects': last_hightest_rate_projects,
                'images': images,
                'categories': Category.objects.all(),
                'projects_count': len(Project.objects.all()),
                'donors_count': len(Donation.objects.all()),
                'last_5': last_5_projects,
                "user": RegisterUser.objects.get(user_id=request.session['user_id']),
                'last_5_featured': last_5_featured_projects
            })
        except:
            return HttpResponseRedirect('/homePage')
    else:
        return redirect('login')


def getAllMyProjects(request):
    if 'user_id' in request.session:
        try:
            if 'user_id' not in request.session:
                return HttpResponseRedirect('logIn')
            else:
                projects = Project.objects.filter(
                    user_id=request.session['user_id']).all()
                images = []
                for project in projects:
                    images.append(project.image_set.all().first().images.url)
                context = {
                    "user": RegisterUser.objects.get(user_id=request.session['user_id']),
                    'show': 'my projects',
                    'projects': projects,
                    'images': images,
                    'categories': Category.objects.all(),
                }
                return render(request, "home/show_categories.html", context)
        except:
            return HttpResponseRedirect('/homePage')
    else:
        return redirect('login')


def categoryProjects(request, cat_id):
    if 'user_id' in request.session:
        try:
            cat = Category.objects.filter(id=cat_id)
            if cat:
                projects = Project.objects.filter(
                    category_id=cat_id).all()
                images = []
                for project in projects:
                    images.append(project.image_set.all().first().images.url)
                context = {
                    "user": RegisterUser.objects.get(user_id=request.session['user_id']),
                    'show': 'show project by category ' + Category.objects.get(id=cat_id).name,
                    'projects': projects,
                    'images': images,
                    'categories': Category.objects.all(),
                }
                return render(request, "home/show_categories.html", context)
            else:
                return HttpResponseRedirect('/homePage')
        except:
            return HttpResponseRedirect('/homePage')
    else:
        return redirect('login')


def search(request):
    if 'user_id'  in request.session:
        try:
            search_post = request.POST['search']
            if search_post:
                projects = Project.objects.filter(title__icontains=search_post)
                searched_tags = Tag.objects.filter(name__icontains=search_post)
                images = []
                for project in projects:
                    images.append(project.image_set.all().first().images.url)
                context = {
                    "user": RegisterUser.objects.get(user_id=request.session['user_id']),
                    'projects': projects,
                    'tags': searched_tags,
                    'images': images,
                    'show': 'search about ' + search_post,
                    'categories': Category.objects.all(),
                }
                return render(request, "home/show_categories.html", context)
            else:
                return redirect('home')
        except:
            return redirect('home')
    else:
        return redirect('login')


def tagProjects(request, tag_id):
    if 'user_id' in request.session:
        try:
            tag = Tag.objects.filter(id=tag_id)
            if tag:
                projects = tag[0].project_set.all()
                images = []
                for project in projects:
                    images.append(project.image_set.all().first().images.url)

                context = {
                    "user": RegisterUser.objects.get(user_id=request.session['user_id']),
                    'projects': projects,
                    'images': images,
                    'show': 'show project by tag ' + tag[0].name,
                    'categories': Category.objects.all(),
                }
                return render(request, "home/show_categories.html", context)
            else:
                return HttpResponseRedirect('/homePage')
        except:
            return HttpResponseRedirect('/homePage')
    else:
        return redirect('login')