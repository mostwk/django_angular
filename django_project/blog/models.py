from django.db import models
from django_project.authentication.models import Account
from django.contrib.contenttypes.fields import GenericRelation
from django_project.likes.models import Like


class BlogPost(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=120)
    body = models.TextField(default='', max_length=500)
    comments = models.IntegerField(default=0)
    likes = GenericRelation(Like)

    class Meta:
        ordering = ('create_date', )

    def __str__(self):
        return self.name

    @property
    def total_likes(self):
        return self.likes.count()


class PostComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like)

    class Meta:
        ordering = ('pk', )

    def __str__(self):
        return self.text

    @property
    def total_likes(self):
        return self.likes.count()

