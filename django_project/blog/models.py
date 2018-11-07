from django.db import models
from django.utils import timezone
from django_project.authentication.models import Account


class BlogPost(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=120)
    body = models.TextField(default='', max_length=500)

    def __str__(self):
        return self.name
