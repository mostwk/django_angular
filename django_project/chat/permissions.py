from rest_framework import permissions

from .models import ChatSession


class IsChatMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            uri = view.kwargs['uri']
            chat_session = ChatSession.objects.get(uri=uri)
            members = [
                chat_session.user.username
                for chat_session in chat_session.members.all()
            ]
            return request.user.username in members or request.user == chat_session.owner
        return False
