from django.contrib import admin
from django_project.blog.models import BlogPost, PostComment

admin.site.register(BlogPost)
admin.site.register(PostComment)