from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (ChatSession, ChatSessionMember, ChatSessionMessage,
                     deserialize_user)


class ChatSessionView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user

        chat_session = ChatSession.objects.create(owner=user)

        return Response({
            'status': 'Success',
            'uri': chat_session.uri,
            'message': 'New chat session created'
        })

    def patch(self, request, *args, **kwargs):
        """
        Add user to a chat session
        """
        User = get_user_model()

        uri = kwargs['uri']
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
            deserialize_user(chat_session.user)
            for chat_session in chat_session.member.all()
        ]
        members.insert(0, owner)

        return Response({
            'status': 'Success',
            'members': members,
            'message': f'{user.username} joined the chat',
            'user': deserialize_user(user)
        })


class ChatSessionMessageView(APIView):

    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
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
            'uri': chat_session.uri,
            'messages': messages
        })

    def post(self, request, *args, **kwargs):
        """
        Create a new message in a chat session
        """
        uri = kwargs['uri']
        message = request.date['message']

        user = request.user
        chat_session = ChatSession.objects.get(uri=uri)

        ChatSessionMessage.objects.create(
            user=user, chat_session=chat_session, message=message
        )

        return Response({
            'status': 'Success',
            'uri': chat_session.uri,
            'message': message,
            'user': deserialize_user(user)
        })
