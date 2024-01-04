from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, render, redirect

from core.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from django.conf import settings
from django.shortcuts import redirect

import datetime
from core.models import Post, Category


def RegisterView(request):
    if request.method == "POST":
        data = request.POST
        fname = data.get("first_name")
        lname = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        is_author = data.get("is_author")

        try:
            user = User.objects.create(
                first_name=fname,
                last_name=lname,
                email=email,
                is_author=is_author,
            )
            user.set_password(password)
            user.save()
            return redirect("/account/login/")
        except Exception as e:
            print(e)
            return HttpResponse("error occured! try again!")
    else:
        if request.session.exists(request.session.session_key):
            return redirect("/account/dashboard/")
        else:
            print(request.session.session_key)
            return render(request, "register.html")


def LoginView(request):
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect("/account/dashboard/")
        else:
            return HttpResponse("credentials not match!")
    else:
        return render(request, "login.html")


def DashboardView(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    else:
        return render(request, "dashboard/dashboard.html")


def AddNewBlogView(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    else:
        user = request.user
        userid = user.id
        category = Category.objects.all()
        print(category)
        context = {"userid": userid, "category": category}
        return render(request, "dashboard/addnew.html", context)


def SavePostView(request):
    if request.method == "POST":
        data = request.POST
        userid = request.user.id
        post_title = data.get("title")
        thumb_img = request.FILES["thumbimg"]
        post_descp = data.get("post_description")
        body_img = request.FILES["bodyimg"]
        categoryid = data.get("category")

        category = get_object_or_404(Category, id=categoryid)

        try:
            post = Post.objects.create(
                post_title=post_title,
                post_author=request.user,
                post_category=category,
                post_body=post_descp,
                post_thumbnail_img=thumb_img,
                post_body_img=body_img,
                date_published=datetime.datetime.now(),
            )
            post.save()

            return redirect("/account/dashboard/")

        except Exception as e:
            print(e)
            return HttpResponse("SOME ERROR OCCURED! TRY AGAIN!")

    else:
        return HttpResponse("plz send a valid request!")


def AllPostsView(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    else:
        user = request.user
        userid = user.id
        post = Post.objects.filter(post_author=request.user)
        context = {"post": post}
        return render(request, "dashboard/allposts.html", context)


def EditPostView(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    else:
        if request.method == "POST":
            data = request.POST
            postid = data.get("postid")
            if (
                Post.objects.filter(post_author=request.user)
                and request.user.is_authenticated
            ):
                post = Post.objects.select_related("post_category").get(id=postid)
                category = Category.objects.all()
                context = {"post": post, "category": category}
                return render(request, "dashboard/editpost.html", context)
            else:
                return HttpResponse("error occured!")
        else:
            return HttpResponse("send valid request!")


def SaveEditPostView(request):
    if request.method == "POST":
        data = request.POST

        post_title = data.get("title")
        post_descp = data.get("post_description")
        postid = data.get("postid")
        catid = data.get("category")

        category = get_object_or_404(Category, id=catid)

        try:
            if Post.objects.filter(id=postid).exists():
                post = Post.objects.get(id=postid)

                post.post_title = post_title
                post.post_author = request.user
                post.post_body = post_descp
                post.post_category = category

                try:
                    post.post_thumbnail_img = request.FILES["thumbimg"]
                except Exception as e:
                    print(e)

                try:
                    post.post_body_img = request.FILES["bodyimg"]
                except Exception as e:
                    print(e)

                post.save()

                return redirect("/account/dashboard/")
            else:
                return HttpResponse("postid not exist!")

        except Exception as e:
            print(e)
            return HttpResponse("SOME ERROR OCCURED! TRY AGAIN!")
    else:
        return HttpResponse("invalid request!")


def DeletePostView(request):
    if request.method == "POST":
        data = request.POST
        postid = data.get("deletepostid")
        if Post.objects.filter(id=postid).exists():
            post = Post.objects.get(id=postid)
            try:
                if post.delete():
                    return redirect("/account/dashboard/")
                else:
                    return HttpResponse("SOME ERROR OCCURED! Post Can't Deleted!")
            except Exception as e:
                print(e)
        else:
            return HttpResponse("post id does not exist! ")
        return HttpResponse("delete request")
    else:
        return HttpResponse("invalid request!")


def LogoutView(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    else:
        logout(request)
        return redirect("/")
