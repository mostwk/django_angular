from rest_framework import serializers
from .models import BlogPost, PostComment


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'date', 'author', 'name', 'body', 'comments')


class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = PostComment
        fields = ('id', 'author', 'text', 'date', 'post_id')
