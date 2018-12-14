from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'chats', views.ChatSessionView, basename='chat')
router.register(r'chats/(?P<uri>.+?)/messages', views.ChatSessionMessageView, basename='chat-message')

urlpatterns = router.urls
