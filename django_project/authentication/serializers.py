from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirmed_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirmed_password',)
        read_only_fields = ('created_at', 'updated_at',)

    def validate(self, data):
        if len(data['username']) < 5:
            raise serializers.ValidationError(
                _('Username should be at least 5 characters')
            )
        if data['confirmed_password'] != data['password']:
            raise serializers.ValidationError(
                _('Passwords are not identical')
            )
        if len(data['password']) < 6:
            raise serializers.ValidationError(
                _('Password must be at least 6 characters')
            )
        return data

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)

        instance.save()

        password = validated_data.get('password', None)
        confirmed_password = validated_data.get('confirmed_password', None)

        if password and confirmed_password and password == confirmed_password:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)

        return instance
