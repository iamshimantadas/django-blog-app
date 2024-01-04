from django.shortcuts import render, redirect
from django.urls import reverse

from core.models import Post
from core.models import Comment

from django.http import HttpResponse
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

from django.conf import settings

from django.http import HttpResponseRedirect

def PostView(request):
    # if pk:
    #     id = pk
    #     if Post.objects.filter(id=id).exists():
    #             post = Post.objects.select_related('post_author').select_related('post_category').get(id=id)
    #             cmnt = Comment.objects.filter(post_id=id).select_related('post_id')
    #             context = {"post":post,"comment":cmnt}
    #             return render(request,"post-detail.html",context)
    #     else:
    #             return HttpResponse("post id not exist!")
    # else:
    #     if request.method == "POST":
    #         data = request.POST
    #         id = data.get("postid")
    #         if Post.objects.filter(id=id).exists():
    #             post = Post.objects.select_related('post_author').select_related('post_category').get(id=id)
    #             cmnt = Comment.objects.filter(post_id=id).select_related('post_id')
    #             context = {"post":post,"comment":cmnt}
    #             return render(request,"post-detail.html",context)
    #         else:
    #             return HttpResponse("post id not exist!") 
    #     else:
    #         return HttpResponse("invalid request!")
    
    if request.method == "GET":
        data = request.GET
        id = data.get("postid")
        if Post.objects.filter(id=id).exists():
            post = Post.objects.select_related('post_author').select_related('post_category').get(id=id)
            cmnt = Comment.objects.filter(post_id=id).select_related('post_id')
            context = {"post":post,"comment":cmnt}
            return render(request,"post-detail.html",context)
        else:
            return HttpResponse("post id not exist!") 
    else:
        return HttpResponse("invalid request!")


def AllPostsView(request):
        post = Post.objects.select_related('post_author').select_related('post_category')
        paginator = Paginator(post, 2) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request,"posts.html",context={"post": page_obj})


# comment box
def CommentView(request):
    if request.method == "POST":
        data = request.POST
        postid = data.get('postid')
        name = data.get('name')
        email = data.get('email')
        comment_body = data.get('comment')

        try:
            validate_email(email)
        except ValidationError as e:
            print("bad email, details:", e)
            return HttpResponse("please enter appropriate email adress! ")
        else:
            print("good email")
            cmnt = Comment.objects.create(
            post_id_id = postid,
            comment_author_name = name,
            comment_author_email = email,
            comment = comment_body,
            date_of_comment = timezone.now()
            )
            cmnt.save()

            if Post.objects.filter(id=postid).exists():        
                # post = Post.objects.select_related('post_author').get(id=postid)
                # cmnt = Comment.objects.filter(post_id=postid).select_related('post_id')
                # context = {"post":post,"comment":cmnt}
                # return render(request,"pages/post-detail.html",context)
                return redirect('/')
            else:
                return HttpResponse("post id not exist!") 

    else:
        return HttpResponse("comment not added")


def AboutView(request):
    return render(request,"about.html")

def SearchBlogView(request):
        data = request.GET
        search_string = data.get("query")

        if Post.objects.filter(post_title__contains=search_string).exists():
            search_posts = Post.objects.filter(post_title__contains=search_string)
            if search_posts.exists():
                # Iterating through the queryset to get IDs of matching posts
                matching_post = [post.id for post in search_posts]
                postid = matching_post[0]

                post = Post.objects.select_related('post_author').select_related('post_category').get(id=postid)
                cmnt = Comment.objects.filter(post_id=postid).select_related('post_id')
                context = {"post":post,"comment":cmnt}
                return render(request,"post-detail.html",context)
            else:
                return HttpResponse("We didn't find any blog related to: {}".format(search_string))     
        else:
            return HttpResponse("no post match found!")
        

def LikePostView(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        try:
            postid = data.get("postid")
            post = Post.objects.get(id=postid)
            post.likes.add(request.user)
            
            # Use reverse to dynamically generate the URL for 'post-view'
            post_view_url = reverse('post-view')
            # Append the postid as a parameter in the URL
            post_view_url += f'?postid={postid}'

            # Redirect to 'post-view' with the appropriate postid parameter
            return redirect(post_view_url)

        except Exception as e:
            print(e)
            # return HttpResponse("error occured!")
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    else:   
        return HttpResponse("invalid request")    
