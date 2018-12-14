from django.contrib.auth import get_user_model
from notifications.signals import notify
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChatSession, ChatSessionMessage, deserialize_user
from .permissions import IsChatMember


class ChatSessionView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        """
        Create new chat session
        """
        user = request.user
        name = request.data['name']
        chat_session = ChatSession.objects.create(owner=user, name=name)
        create_date = chat_session.create_date
        return Response({
            'status': 'Success',
            'uri': chat_session.uri,
            'create_date': create_date,
            'message': f'{name} session created'
        })

    def partial_update(self, request, *args, **kwargs):
        """
        Add user to a chat session
        """
        User = get_user_model()
        uri = kwargs['pk']
        username = request.data['username']
        user = User.objects.get(username=username)

        chat_session = ChatSession.objects.get(uri=uri)
        owner = chat_session.owner

        if owner != user:
            chat_session.members.get_or_create(
                user=user, chat_session=chat_session
            )

        owner = deserialize_user(owner)
        members = [
            chat_session.user.username
            for chat_session in chat_session.members.all()
        ]
        members.insert(0, owner['username'])

        return Response({
            'status': 'Success',
            'members': members,
            'message': f'{user.username} joined the chat',
            'user': deserialize_user(user)
        })

    @action(methods=['GET'], detail=True)
    def members(self, request, *args, **kwargs):
        uri = kwargs['pk']
        chat_session = ChatSession.objects.get(uri=uri)
        members = [
            chat_session.user.username
            for chat_session in chat_session.members.all()
        ]
        return Response({
            'status': 'Success',
            'uri': chat_session.uri,
            'name': chat_session.name,
            'owner': chat_session.owner.username,
            'count': len(members),
            'members': members
        })


class ChatSessionMessageView(viewsets.ModelViewSet):

    permission_classes = (IsChatMember, )

    def list(self, request, *args, **kwargs):
        """
        Return all messages from a chat session
        """
        uri = kwargs['uri']

        chat_session = ChatSession.objects.get(uri=uri)
        messages = [
            chat_session_message.to_json()
            for chat_session_message in chat_session.messages.all()
        ]

        return Response({
            'status': 'Success',
            'uri': chat_session.uri,
            'name': chat_session.name,
            'owner': chat_session.owner.username,
            'messages': messages
        })

    def create(self, request, *args, **kwargs):
        """
        create a new message in a chat session.
        """
        uri = kwargs['uri']
        message = request.data['message']

        user = request.user
        chat_session = ChatSession.objects.get(uri=uri)

        chat_session_message = ChatSessionMessage.objects.create(
            user=user, chat_session=chat_session, message=message
        )

        notif_args = {
            'source': user,
            'source_display_name': user.get_full_name(),
            'category': 'chat', 'action': 'Sent',
            'obj': chat_session_message.id,
            'short_description': 'You a new message', 'silent': True,
            'extra_data': {
                'uri': chat_session.uri,
                'message': {
                    'date_created': chat_session_message.create_date,
                    'user': deserialize_user(user),
                    'message': message
            }}
        }
        notify.send(
            sender=self.__class__, **notif_args, channels=['websocket']
        )

        return Response({
            'status': 'Success',
            'uri': chat_session.uri,
            'message': message,
            'user': deserialize_user(user)
        })
