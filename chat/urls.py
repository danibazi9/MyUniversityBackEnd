from django.urls import path

from . import api

app_name = 'chat'
urlpatterns = [
    path('chat-list/', api.ChatList.as_view()),
    path('chat-list/<int:stuID>', api.ChatDetails.as_view()),
]
