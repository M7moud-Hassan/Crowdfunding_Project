from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from projects_app.models import Project, Donation, Category, Tag
from django.db.models import Avg
from django.http import HttpResponseRedirect



@require_http_methods(["GET"])
def home(request):
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
            'last_5_featured': last_5_featured_projects
            })
    except:
        return HttpResponseRedirect('/homePage')
def getAllMyProjects(request):
    try:
        request.session['user_id'] = 2
        if 'user_id' not in request.session:
            return HttpResponseRedirect('logIn')
        else:
            projects = Project.objects.filter(
                    user_id=request.session['user_id']).all()
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
                'show':'my projects',
                'projects': projects,
                'images': images,
                'categories': Category.objects.all(),
            }
            return render(request, "home/show_categories.html", context)
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