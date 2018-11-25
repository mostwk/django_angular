from rest_framework.decorators import action
from rest_framework.response import Response

from . import services
from .serializers import WhoLikedSerializer


class LikedMixin:

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None, **kwargs):
        """
        Like specific object
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response({
            'status': 'Success',
        })

    @action(methods=['POST'], detail=True)
    def unlike(self, request, pk=None, **kwargs):
        """
        Unlike specific object
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response({
            'status': 'Success',
        })

    @action(methods=['GET'], detail=True)
    def who_liked(self, request, pk=None, **kwargs):
        """
        Return list of users who liked specific object
        """
        obj = self.get_object()
        fans = services.get_who_liked(obj)
        serializer = WhoLikedSerializer(fans, many=True)
        result = [user['username'] for user in serializer.data]
        return Response({
            'status': 'Success',
            'users': result
        })
