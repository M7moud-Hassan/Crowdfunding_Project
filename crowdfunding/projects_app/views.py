from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import *
from .models import *
from django.db.models import Avg, Sum


@require_http_methods(["GET", "POST"])
def createProject(req):
    req.session['user_id']=2
    if 'user_id' not in req.session:
        pass
    else:
        user =User.objects.get(id=req.session['user_id'])
        if req.method == 'GET':
            form = ProjectForm()
            return render(req, "projects/add_project.html",
                          context={"form": form})

        if req.method == "POST":
            if "tag" in req.POST or req.POST['newTag'] != "":
                if req.POST['newTag'] != '':
                    new_tag = Tag.objects.create(name=req.POST['newTag']).id
                    req.POST = req.POST.copy()
                    req.POST.update({
                        "tag": new_tag
                    })
            form = ProjectForm(req.POST, req.FILES)
            images = req.FILES.getlist('images')
            if form.is_valid():
                project = form.save(commit=False)
                project.user = user
                project.save()
                form.save_m2m()
                for image in images:
                    Image.objects.create(project_id=project.id, images=image)
                return render(req,'base_page.html')
        else:
            form = ProjectForm()
        return render(req, "projects/add_project.html", context={"form": form, "user": user})

@require_http_methods(["GET"])
def projectDetails(req, project_id):
    req.session['user_id'] = 1
    if 'user_id' not in req.session:
       pass
    else:
        user =User.objects.get(id=req.session['user_id'])
        project = Project.objects.get(id=project_id)
        donate_sum = project.donation_set.all().aggregate(Sum("donation"))
        donations_count = len(project.donation_set.all())
        donation_average = (donate_sum["donation__sum"] if donate_sum["donation__sum"] else 0) * 100 / project.total_target

        #get cimments and replay
        comments_project = project.comment_set.all()
        replies_all = Reply.objects.all()

        #get tags
        tags_project = project.tag.all()
        related_projects_tags = []
        for tag in tags_project:
            related_projects_tags.append(tag.project_set.all())

        #get images project
        project_images = project.image_set.all()
        counter_images = []
        for image in project_images:
            counter_images.append("1")
        counter_images.pop()

        # get 4 projects have same tags
        related_projects = Project.objects.none().union(*related_projects_tags)[:4]
        related_projects_images = []
        for related_project in related_projects:
            related_projects_images.append(related_project.image_set.all().first().images.url)


        #date format and remender days
        data_format = "%Y-%m-%d %H:%M:%S"
        today = datetime.strptime(datetime.now().strftime(data_format), data_format)
        end_date = datetime.strptime(project.end_time.strftime(data_format), data_format)
        days_diff = (end_date - today).days
        reply = ReplyForm()
        #avrage rate project
        average_rating = project.rate_set.all().aggregate(Avg('rate'))['rate__avg']

        # return user rating if found on project
        user_rating = 0
        prev_rating = Rate.objects.filter(user_id=user.id,projcet=project)
        if prev_rating:
            user_rating = prev_rating[0].rate
        if average_rating is None:
            average_rating = 0

        #send data to template
        context = {
            'project': project,
            'donation': donate_sum["donation__sum"] if donate_sum["donation__sum"] else 0,
            'donations': donations_count,
            'days': days_diff,
            'comments': comments_project,
            'project_images': project_images,
            'replies': replies_all,
            'related_projects': related_projects,
            'images': related_projects_images,
            'check_target': project.total_target * .25,
            'donation_average': donation_average,
            'rating': average_rating * 20,
            'tags': tags_project,
            'reply_form': reply,
            'user_rating': user_rating,
            'rating_range': range(5, 0, -1),
            'average_rating': average_rating,
            'user': user,
            'counter': counter_images
        }
        return render(req, "projects/project_details.html", context)

@require_http_methods(["POST"])
def deleteProject(req, project_id):
    if 'user_id' not in req.session:
        pass
    else:
        project = get_object_or_404(Project, pk=project_id)
        project.delete()

@require_http_methods(["POST"])
def addComment(req, project_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        pass
    else:
        user = User.objects.get(id=req.session['user_id'])
        if req.POST['comment']:
            Comment.objects.create(
                comment=req.POST['comment'],
                project_id=project_id,
                user_id=user.id
            )
            return redirect('project_details', project_id)

@require_http_methods(["POST"])
def addReport(req, project_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        pass
    else:
        user = User.objects.get(id=req.session['user_id'])
        project = Project.objects.get(id=project_id)
        ProjectReport.objects.create(
            project=project,
            user_id=user.id
        )
        return redirect('project_details', project_id)

@require_http_methods(["POST"])
def addCommentReport(req, comment_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        pass
    else:
        user = User.objects.get(id=req.session['user_id'])
        my_comment = Comment.objects.get(id=comment_id)
        project = Project.objects.all().filter(comment__id=comment_id)[0]
        CommentReport.objects.create(
            comment=my_comment,
            user_id=user.id
        )
        return redirect('project_details', project.id)

@require_http_methods(["POST"])
def addDonate(req, project_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        user = User.objects.get(id=req.session['user_id'])
        if req.POST['donate']:
            Donation.objects.create(
                donation=req.POST['donate'],
                project_id=project_id,
                user_id=user.id,
            )
            return redirect('project_details', project_id)

@require_http_methods(["POST"])
def rateProject(req, project_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
       pass
    else:
        user = User.objects.get(id=req.session['user_id'])
        project = get_object_or_404(Project, pk=project_id)
        rate = req.POST.get('rate', '')
        if rate:
            prev_user_rating = project.rate_set.filter(user_id=user.id)
            if prev_user_rating:
                prev_user_rating[0].rate = int(rate)
                prev_user_rating[0].save()
            else:
                Rate.objects.create(
                    rate=rate, projcet_id=project.id, user_id=user.id)
        return redirect('project_details', project_id)

@require_http_methods(["POST"])
def commentReply(req, comment_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        pass
    else:
        project = Project.objects.all().filter(comment__id=comment_id)[0]
        user = User.objects.get(id=req.session['user_id'])
        if req.POST['reply']:
                Reply.objects.create(
                    reply=req.POST['reply'],
                    comment_id=comment_id,
                    user_id=user.id
                )
                return redirect('project_details', project.id)