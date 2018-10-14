from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework import viewsets, permissions


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def create(self, serializer):
        serializer.save(user=self.request.user)
