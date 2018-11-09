from .models import BlogPost
from .serializers import BlogPostSerializer
from .permissions import IsPostAuthor
from rest_framework import viewsets, permissions
from django_project.authentication.views import MyTokenAuthentication
from rest_framework.response import Response
from rest_framework import status


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = (MyTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),

        if self.request.method == 'POST':
            return permissions.IsAuthenticated(),

        if self.request.method == 'DELETE':
            return IsPostAuthor(),

        return permissions.IsAuthenticated(), IsPostAuthor(),

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'status': 'Success',
                'post': serializer.data},
                status=status.HTTP_201_CREATED, headers=headers)
        return Response({
            'status': 'Bad request',
            'error': 'Name and body fields may not be blank'
        }, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
