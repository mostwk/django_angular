from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def deserialize_user(user):
    return {
        'username': user.username
    }


class TrackableDateModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def generate_unique_uri():
    return str(uuid4()).replace('-', '')[:15]


class ChatSession(TrackableDateModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    uri = models.URLField(default=generate_unique_uri)


class ChatSessionMessage(TrackableDateModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    chat_session = models.ForeignKey(
        ChatSession, related_name='messages', on_delete=models.PROTECT
    )
    message = models.TextField(max_length=200)

    def to_json(self):
        return {
            'user': deserialize_user(self.user),
            'message': self.message
        }


class ChatSessionMember(TrackableDateModel):
    chat_session = models.ForeignKey(
        ChatSession, related_name='member', on_delete=models.PROTECT
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
