from django.contrib import admin

from core.models import User
from core.models import Post
from core.models import Comment, Category

from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    ordering = (
        "email",
        "id",
    )

    list_display = (
        "first_name",
        "last_name",
        "email",
        
        "is_staff",
        "is_superuser",
        "is_active",
    )

    search_fields = ("first_name", "last_name", "email")

    list_filter = ("is_staff", "is_active")

    # list_editable = ("is_staff", "is_superuser", "is_active")

    exclude = ("username", "date_joined")

    add_fieldsets = (
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Contact Info",
            {
                "fields": ("email", ),
            },
        ),
        (
            "Password",
            {
                "fields": (
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    fieldsets = (
        (
            "Contact Info",
            {
                "fields": (
                    "email",
                    
                )
            },
        ),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                ),
                "classes": ["wide", "extrapretty"],
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
        ("Password", {"fields": ("password",)}),
    )



admin.site.register(User, AccountAdmin)


# post model 
class PostAdmin(admin.ModelAdmin):
    list_display = ['post_title','post_author','date_published']
    # search_fields = ('post_title', 'post_author__username')
    list_display_links = ('post_title',)
    list_filter = ('post_author',)

admin.site.register(Post,PostAdmin)

admin.site.register(Category)



class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_author_name','comment_author_email','date_of_comment','comment']

admin.site.register(Comment, CommentAdmin)
