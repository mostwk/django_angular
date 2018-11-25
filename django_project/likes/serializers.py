from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class WhoLikedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
        )

    def get_username(self, obj):
        return obj.get_username()
