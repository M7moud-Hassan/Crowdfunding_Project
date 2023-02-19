from django.shortcuts import render
from projects_app.models import Project
from django.db.models import Avg
# Create your views here.
def home(request):
    last_hightest_rate_projects=Project.objects.annotate(avg_rate=Avg('rate__rate')).order_by('avg_rate')[:5]
    images=[]
    for p in last_hightest_rate_projects:
        print(p.image_set.all().first)
        images.append(p.image_set.all().first().images.url)
    last_5_projects=Project.objects.all()[:5]
    last_5_featured_projects=Project.objects.filter(is_featured=True).order_by('id')[:5]
    return render(request,'home/home_page.html',context={
        'projects':last_hightest_rate_projects,
        'images':images,
        'last_5':last_5_projects,
        'last_5_featured':last_5_featured_projects
    })