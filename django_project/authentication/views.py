from rest_framework import viewsets, permissions
from .models import Account
from .serializers import AccountSerializer
from .permissions import IsAccountOwner
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
import json


class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),

        if self.request.method == 'POST':
            return permissions.AllowAny(),

        if self.request.method == 'DELETE':
            return IsAccountOwner(),

        return permissions.IsAuthenticated(), IsAccountOwner(),

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)
            del serializer.validated_data['password']
            del serializer.validated_data['confirmed_password']
            return Response({
                'status': 'Success',
                'message': 'Hello',
                'user': serializer.validated_data
            }, status=status.HTTP_201_CREATED)

        removed_duplicates = [key + ': ' + value[0] for key, value in
                              serializer.errors.items() if 'blank' in value[0]]
        error_list = [value[0] for key, value in
                      serializer.errors.items() if 'blank' not in value[0]]
        error_list.extend(removed_duplicates)
        return Response({
            'status': 'Bad request',
            'errors': error_list
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            update_last_login(None, token.user)
            return Response({
                'status': 'Success',
                'token': token.key,
                'user': {
                    'email': token.user.email,
                    'username': token.user.username,
                    'first_name': token.user.first_name,
                    'last_name': token.user.last_name
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": 'Bad request',
            'error': "Could not log in with provided credentials"
        }, status=status.HTTP_400_BAD_REQUEST)
