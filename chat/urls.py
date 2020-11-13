from django.urls import path

from . import views, api

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    # path('chat-room-list/<int:stuID>', api.ChatDetails.as_view()),
    # path('chat-contact-list/', api.ContactList.as_view()),
    # path('chat-contacts-list/<int:stuID>', api.ContactDetails.as_view()),
]
