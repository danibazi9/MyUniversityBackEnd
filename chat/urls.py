from django.urls import path, re_path

from . import api

app_name = 'chat'
urlpatterns = [
    path('chat-room-list/', api.ChatList.as_view()),
    path('chat-room-list/<int:stuID>', api.ChatDetails.as_view()),
    path('chat-contact-list/', api.ContactList.as_view()),
    # path('chat-contacts-list/<int:stuID>', api.ContactDetails.as_view()),
]
