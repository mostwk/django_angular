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

        return permissions.IsAuthenticated(), IsAccountOwner,

    def create(self, request):
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
        return Response({
            'status': 'Bad request',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class NewAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=result.data['token'])
        update_last_login(None, token.user)
        return result

