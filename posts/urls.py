from django.urls import path

from .views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',AllPostsView),
    path('post-view',PostView,name="post-view"),
    path('comment/',CommentView, name="comment_box"),
    path('about/',AboutView),
    path('search',SearchBlogView,name="search_blog"),
    path('like',LikePostView,name="postlike")
] 