from rest_framework import serializers

from django_project.likes import services as likes_services

from .models import BlogPost, PostComment


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ('id', 'create_date', 'update_date',
                  'author', 'name', 'body', 'comments', 'total_likes', 'is_liked')

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance

    def get_is_liked(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_liked(obj, user)


class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ('id', 'author', 'text',
                  'create_date', 'update_date', 'post_id', 'total_likes', 'is_liked')

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        return instance

    def get_is_liked(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_liked(obj, user)
