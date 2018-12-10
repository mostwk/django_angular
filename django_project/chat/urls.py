from django.contrib import admin
from django.urls import path

from . import views

# urlpatterns = [
#     path(r'chats/', views.ChatSessionView.as_view({'post': 'create'})),
#     path(r'chats/<uri>/', views.ChatSessionView.as_view({'patch': 'partial_update'})),
#     path(r'chats/<uri>/messages/', views.ChatSessionMessageView.as_view({'post': 'create', 'get': 'list'})),
#     path(r'chats/<uri>/members', views.ChatSessionView.as_view({'get': 'members'}))
# ]
urlpatterns = [
    path('chats/', views.ChatSessionView.as_view()),
    path('chats/<uri>/', views.ChatSessionView.as_view()),
    path('chats/<uri>/messages/', views.ChatSessionMessageView.as_view()),
]
