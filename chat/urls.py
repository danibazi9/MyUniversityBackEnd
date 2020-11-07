from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import api

app_name = 'MyUniversity'
urlpatterns = [
    path('chat-list/', api.ChatList.as_view()),
    path('chat-list/<int:stuID>', api.ChatDetails.as_view()),
]
