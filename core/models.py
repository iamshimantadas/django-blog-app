from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.contrib.auth.models import PermissionsMixin


from core.managers import *

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(max_length=200, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

class Category(models.Model):
    cat_name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.cat_name    

class Post(models.Model):
    post_title = models.CharField(max_length=255)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_body = models.TextField()
    post_thumbnail_img = models.ImageField(upload_to="media/posts/")
    post_body_img = models.ImageField(upload_to="media/posts")
    post_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_published = models.DateTimeField()
    likes = models.ManyToManyField(User,related_name="like", null=True)

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author_name = models.CharField(max_length=50)
    comment_author_email = models.EmailField()
    comment = models.TextField()
    date_of_comment = models.DateTimeField()

    def __str__(self):
        return self.comment_author_name
    



    
    
