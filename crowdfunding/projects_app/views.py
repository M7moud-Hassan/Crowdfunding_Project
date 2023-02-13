from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View

from .forms import *
from .models import *
from django.template import loader
from django.db.models import Avg, Sum
import re
NULL={}

def createProject(req):
    req.session['user_id']=2
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        user =User.objects.get(id=req.session['user_id'])
        if req.method == 'GET':
            form = ProjectForm()
            return render(req, "projects/add_project.html",
                          context={"form": form})

        if req.method == "POST":
            tag_error = ''
            if "tag" in req.POST or req.POST['newTag'] != "":
                if req.POST['newTag'] != '':
                    new_tag = Tag.objects.create(name=req.POST['newTag']).id
                    req.POST = req.POST.copy()
                    req.POST.update({
                        "tag": new_tag
                    })
            else:
                tag_error = "Please add tag"
            form = ProjectForm(req.POST, req.FILES)
            if tag_error != "":
                form.add_error('tag', tag_error)

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


def projectDetails(req, project_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        user =User.objects.get(id=req.session['user_id'])
    try:
        project = Project.objects.get(id=project_id)
        donate = project.donation_set.all().aggregate(Sum("donation"))
        donations_count = len(project.donation_set.all())
        comments = project.comment_set.all()
        replies = Reply.objects.all()
        project_images = project.image_set.all()
        counter = []
        for image in project_images:
            counter.append("1")
        counter.pop()
        tags = project.tag.all()


        myFormat = "%Y-%m-%d %H:%M:%S"
        today = datetime.strptime(datetime.now().strftime(myFormat), myFormat)
        end_date = datetime.strptime(project.end_time.strftime(myFormat), myFormat)
        days_diff = (end_date - today).days

        report_form = ReportForm()
        reply = ReplyForm()

        donation_average = (donate["donation__sum"] if donate["donation__sum"] else 0) * 100 / project.total_target
        average_rating = project.rate_set.all().aggregate(Avg('rate'))['rate__avg']

        # return user rating if found
        user_rating = 0

        if 'user_id' in req.session:
            # prev_rating = Project.rate_set.get(user_id=user.id)
            prev_rating = []

            if prev_rating:
                user_rating = prev_rating[0].rate

        if average_rating is None:
            average_rating = 0

        context = {
            'project': project,
            'donation': donate["donation__sum"] if donate["donation__sum"] else 0,
            'donations': donations_count,
            'days': days_diff,
            'comments': comments,
            'project_images': project_images,
            'replies': replies,
            'tags': tags,

            'report_form': report_form,
            'reply_form': reply,

            'check_target': project.total_target * .25,
            'donation_average': donation_average,

            'rating': average_rating * 20,
            'user_rating': user_rating,
            'rating_range': range(5, 0, -1),
            'average_rating': average_rating,

            'user': user,
            'counter': counter
        }
        return render(req, "projects/project_details.html", context)
    except Project.DoesNotExist:
        print('project not exitis')
        return render(req, "/")


def addComment(req, project_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        user = User.objects.get(id=req.session['user_id'])
        if req.method == "POST":
            if req.POST['comment']:
                comment = Comment.objects.create(
                    comment=req.POST['comment'],
                    project_id=project_id,
                    user_id=user.id
                )
                return redirect('project_details', project_id)
        return render(req, "projects/project_details.html", project_id , context={"user":user})


def addReport(req, project_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        user = User.objects.get(id=req.session['user_id'])
        project = Project.objects.get(id=project_id)
        if req.method == "POST":
            ProjectReport.objects.create(
                report='bad',
                project=project,
                user_id=user.id
            )
            return redirect('project_details', project_id)

def addCommentReport(req, comment_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        user = User.objects.get(id=req.session['user_id'])
        my_comment = Comment.objects.get(id=comment_id)
        project = Project.objects.all().filter(comment__id=comment_id)[0]

        if req.method == "POST":
            CommentReport.objects.create(
                report='bad',
                comment=my_comment,
                user_id=user.id
            )
            return redirect('project_details', project.id)


def addDonate(req, project_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        user = User.objects.get(id=req.session['user_id'])
        if req.method == "POST":
            if req.POST['donate']:
                donation = Donation.objects.create(
                    donation=req.POST['donate'],
                    project_id=project_id,
                    user_id=user.id,
                )
                return redirect('project_details', project_id)
        return render(req, "projects/project_details.html", project_id , context={"user":user})
def rateProject(req, project_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        user = User.objects.get(id=req.session['user_id'])
        if req.method == "POST":
            project = get_object_or_404(Project, pk=project_id)
            context = {"project": project}

            rate = req.POST.get('rate', '')

            if rate and rate.isnumeric():
                prev_user_rating = project.rate_set.filter(user_id=user.id)
                if prev_user_rating:
                    prev_user_rating[0].rate = int(rate)
                    prev_user_rating[0].save()

                # first time to rate this project
                else:
                    Rate.objects.create(
                        rate=rate, projcet_id=project.id, user_id=user.id)

        return redirect('project_details', project_id)
def commentReply(req, comment_id):
    req.session['user_id'] = 2
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        project = Project.objects.all().filter(comment__id=comment_id)[0]
        user = User.objects.get(id=req.session['user_id'])
        if req.method == "POST":
            if req.POST['reply']:
                reply = Reply.objects.create(
                    reply=req.POST['reply'],
                    comment_id=comment_id,
                    user_id=user.id
                )
                return redirect('project_details', project.id)
        return render(req, "projects/project_details.html")