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
    except:
        return HttpResponseRedirect('/homePage')