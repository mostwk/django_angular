from .models import BlogPost, PostComment
from .serializers import BlogPostSerializer, PostCommentSerializer
from .permissions import IsPostAuthor, IsCommentAuthor
from rest_framework import viewsets, permissions
from django_project.authentication.views import MyTokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()

    serializer_class = BlogPostSerializer
    authentication_classes = (MyTokenAuthentication, )
    filter_fields = ('name', )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),

        if self.request.method == 'POST':
            return permissions.IsAuthenticated(),

        if self.request.method == 'DELETE':
            return IsPostAuthor(),

        return permissions.IsAuthenticated(), IsPostAuthor(),

    def list(self, request, *args, **kwargs):
        """
        Requesting list of all posts.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        number_of_comments = BlogPost.objects.annotate(count=Count('postcomment'))
        for index, post in enumerate(serializer.data):
            post['comments'] = number_of_comments[index].count
        return Response({
            'status': 'Success',
            'posts': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        pk = self.kwargs['pk']
        number_of_comments = BlogPost.objects.filter(id=pk).annotate(
            count=Count('postcomment'))
        new_data = dict(serializer.data)
        new_data['comments'] = number_of_comments[0].count
        return Response({
            'status': 'Success',
            'post': new_data
        })

    def create(self, request, *args, **kwargs):
        """
        Creating new post if token is provided.
        """
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
        """
        Deleting post if corresponding token is provided.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    authentication_classes = (MyTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),

        if self.request.method == 'POST':
            return permissions.IsAuthenticated(),

        if self.request.method == 'DELETE':
            return IsCommentAuthor(),

        return permissions.IsAuthenticated(), IsCommentAuthor(),

    def list(self, request, *args, **kwargs):
        """
        Returns list of all comments on specified post.
        """
        pk = self.kwargs['post_id']
        queryset = PostComment.objects.filter(post_id=pk)
        count = queryset.count()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'Success',
            'count': count,
            'comments': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        """
        Return specific comment from the post.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'Success',
            'comment': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
        Create new comment to the post
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post_id = kwargs.get('post_id')
            serializer.validated_data['post_id'] = post_id
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'status': 'Success',
                'post': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)

        return Response({
            'status': 'Bad request',
            'error': 'Text field may not be blank'
        }, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, **kwargs):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Deleting comment if corresponding token is provided.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
