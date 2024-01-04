from django.urls import path

from accounts.views import *

urlpatterns = [
    path('',RegisterView),
    path('login/',LoginView),
    path('dashboard/',DashboardView),
    path('dashboard/addnew/',AddNewBlogView),
    path('dashboard/save_post/',SavePostView,name="save_post"),
    path('dashboard/allblogs/',AllPostsView),
    path('dashboard/edit_post/',EditPostView,name="edit_post"),
    path('dashboard/save_edit_post/',SaveEditPostView,name="save_edit_post"),
    path('dashboard/deletepost/',DeletePostView,name="deletepost"),
    path('dashboard/logout/',LogoutView),
]