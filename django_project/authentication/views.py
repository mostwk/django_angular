from django.contrib.auth.models import update_last_login
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .models import Account
from .permissions import IsAccountOwner
from .serializers import AccountSerializer


class MyTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed({
                'status': "Bad request",
                'error': _('Invalid token.')
            })

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed({
                'status': 'Bad request',
                'error': _('User inactive or deleted.')
            })

        return token.user, token


class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (MyTokenAuthentication, )
    filter_fields = ('username', 'email', )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),

        if self.request.method == 'POST':
            return permissions.AllowAny(),

        if self.request.method == 'DELETE':
            return IsAccountOwner(),

        return permissions.IsAuthenticated(), IsAccountOwner(),

    def list(self, request, *args, **kwargs):
        """
        Returns list of all users.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'Success',
            'users': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
        Create new user account if provided information is valid.
        """

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

        error_list = [key + ': ' + value[0]
                      for key, value in serializer.errors.items()
                      ]
        return Response({
            'status': 'Bad request',
            'errors': error_list
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes user account if corresponding token is provided.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """
        Returns authentication token if valid input is provided.
        """
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
                    'username': token.user.username,
                    'email': token.user.email,
                    'first_name': token.user.first_name,
                    'last_name': token.user.last_name
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": 'Bad request',
            'error': "Could not log in with provided credentials"
        }, status=status.HTTP_400_BAD_REQUEST)
