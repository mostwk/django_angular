from django.db import models
from django_project.authentication.models import Account


class BlogPost(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120)
    body = models.TextField(default='', max_length=500)

    class Meta:
        ordering = ('date', )

    def __str__(self):
        return self.name
