from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path(r'chats/', views.ChatSessionView.as_view()),
    path(r'chats/<uri>/', views.ChatSessionView.as_view()),
    path(r'chats/<uri>/messages/', views.ChatSessionMessageView.as_view()),
]