from rest_framework import serializers
from .models import BlogPost, PostComment


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'create_date', 'update_date', 'author', 'name', 'body', 'comments')

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = PostComment
        fields = ('id', 'author', 'text', 'create_date', 'update_date', 'post_id')

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        return instance
