from django.views.decorators.http import require_http_methods
from projects_app.models import Project, Donation
from .models import *
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .form import UserRegistrationForm, LoginForm, EditProfileForm, DeleteAccountForm, PasswordEmailForm, PasswordForm
from django.contrib.auth.decorators import login_required

@require_http_methods(["GET", "POST"])
def register(req):
    req.session.clear()
    if 'user_id' not in req.session:
        if req.method == 'POST':
            form = UserRegistrationForm(req.POST, req.FILES)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['user_email']
                password = form.cleaned_data['user_password']
                phone = form.cleaned_data['user_mobile']
                image = form.cleaned_data['user_image']
                user = RegisterUser.objects.create(first_name=first_name, last_name=last_name, user_email=email,
                                                   user_password=password,
                                                   user_mobile=phone, user_image=image)
                user.is_active = False
                user.save()
                # send verification email
                subject = 'Verify Your Email'
                message = 'Please click the link below to verify your email address: http://localhost:8000/verify/' + str(
                    user.user_id)
                from_email = 'soonfu0@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                msg = 'Please confirm your email address to complete the registration'
                form = LoginForm()
                return render(req, "auth/login.html", context={"login_form": form, "msg": msg, "title": "login"})
        else:
            form = UserRegistrationForm()
        return render(req, 'auth/register.html', context={'form': form,"title":"login"})

    else:
        return redirect("profile")

@require_http_methods(["GET", "POST"])
def login(req):
    if 'user_id' not in req.session:
        msg = None
        if req.method == "POST":
            form = LoginForm(req.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = RegisterUser.objects.filter(user_email=email, user_password=password).first()
                if user is not None:
                    if user.is_active:
                        req.session['user_id'] = user.user_id
                        return redirect("profile")
                    else:
                        msg = "please check your email to activate it !!"
                else:
                    msg = "user doesn't exist "
            else:
                msg = 'Invalid email or password.'
        form = LoginForm()
        return render(req, "auth/login.html", context={"login_form": form, "msg": msg, "title": "login"})
    else:
        return redirect("profile")


@require_http_methods(["GET", "POST"])
def verify_email(req, user_id):
    if 'user_id' not in req.session:
        user = RegisterUser.objects.filter(user_id=user_id).first()
        if user:
            user.is_active = True
            user.save()
        return redirect('login')
    else:return redirect("profile")

@require_http_methods(["GET", "POST"])
def editProfile(req):
    if 'user_id' in req.session:
        user = RegisterUser.objects.filter(user_id=req.session['user_id']).first()
        passw = user.user_password
        if req.method == 'POST':
            if user:
                form = EditProfileForm(req.POST, req.FILES, instance=user)
                if form.is_valid():
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.user_mobile = form.cleaned_data['user_mobile']
                    image = form.cleaned_data['user_image']
                    if image == None:
                        user.user_image = user.user_image
                    else:
                        user.user_image = form.cleaned_data['user_image']
                    if form.cleaned_data['user_password']:
                        user.user_password = form.cleaned_data['user_password']
                    else:
                        user.user_password = passw
                    user.country = form.cleaned_data['country']
                    user.birthdate = form.cleaned_data['birthdate']
                    user.facebook_profile = form.cleaned_data['facebook_profile']

                    user.save()
                    return redirect('profile')
                else:
                    form = LoginForm()
                    return render(req, "auth/login.html", context={"login_form": form})
        else:
            form = EditProfileForm(instance=user)
        return render(req, 'auth/editProfile.html', {'form': form, "user": user, "title": "profile"})
    else:
        return redirect("/")

@require_http_methods(["GET","POST"])
def resetPassword(req):
    if 'user_id' not in req.session:
       if req.method=="POST":
           if req.POST['email']:
               user=RegisterUser.objects.filter(user_email=req.POST['email']).first()
               if user:
                   msg="check your email to set password";
                   subject = 'Verify Your Email'
                   message = 'Please click the link below to set password your account : http://localhost:8000/setpassword/' + \
                             req.POST['email']
                   from_email = 'soonfu0@gmail.com'
                   recipient_list = [req.POST['email']]
                   send_mail(subject, message, from_email, recipient_list)
               else:
                   msg="this email is not register"
               return render(req, 'auth/resetpassword.html', context={
                   "title": "login",
                   "msg":msg,
                   "form": PasswordEmailForm(),
               })
       else:return render(req,'auth/resetpassword.html',context={
            "title":"login",
            "form":PasswordEmailForm(),
        })
    else:
        return redirect("/")


@require_http_methods(["GET"])
def profile(req):
    if 'user_id' in req.session:
        user = RegisterUser.objects.get(user_id=req.session['user_id'])
        projects = Project.objects.filter(user_id=req.session['user_id'])
        donations = Donation.objects.filter(user_id=req.session['user_id'])
        images = []
        for project in projects:
            images.append(project.image_set.all().first().images.url)
        return render(req, 'auth/Profile.html',
                      {"title": "profile", "user": user, "projects": projects, "donations": donations,
                       'images': images,
                       "form_delete": DeleteAccountForm()})
    else:
        return redirect("login")


@require_http_methods(["POST"])
def deleteAccount(req):
    if 'user_id' in req.session:
        if req.method == "POST":
            form = DeleteAccountForm(req.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user = RegisterUser.objects.filter(user_id=req.session['user_id']).first()
                if user is not None:
                    if user.user_password == password:
                        user.is_active = False
                        user.save()
                        # send verification email
                        subject = 'Verify Your Email'
                        message = 'Please click the link below to delete your account : http://localhost:8000/delete/' + str(
                            user.user_id)
                        from_email = 'soonfu0@gmail.com'
                        recipient_list = [user.user_email]
                        send_mail(subject, message, from_email, recipient_list)
                        req.session.clear()
                        return redirect('login')
                    else:
                        return redirect('profile')
    else:
        return redirect('login')


@require_http_methods(["POST"])
def confirmDeleteAccount(req, user_id):
    user = RegisterUser.objects.filter(user_id=user_id).first()
    if user:
        req.session.clear()
        user.delete()
    return redirect('login')

@require_http_methods(["POST","GET"])
def logout(req ):
    req.session.clear()
    return redirect("login" )

@require_http_methods(["GET","POST"])
def sendEmailPassword(req,email):
    if 'user_id' not in req.session:
        if req.method=="POST":
            form = PasswordForm(req.POST)
            if form.is_valid():
                    user = RegisterUser.objects.filter(user_email=email).first()
                    if user:
                            user.user_password = form.cleaned_data['user_password']
                            user.save()
                            return redirect('login')
                    else:
                        return redirect('login')
        else:
            return render(req,'auth/setpassword.html',context={"title":"login","email":email,"form":PasswordForm()})
    else:
        return redirect("login")
