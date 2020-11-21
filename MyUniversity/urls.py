from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import api
import chat.api

app_name = 'MyUniversity'
urlpatterns = [
    path('api/users-list/', api.UsersList.as_view()),
    path('api/users-list/<int:stuID>', api.UsersDetails.as_view()),
    path('api/send-email/<int:stuID>', api.SendEmail.as_view()),
    path('api/chat/', include('chat.urls')),
    path('api/account/', include('account.api.urls', 'account_api')),
    path('api/room-list/', chat.api.chat_properties_view, name='chat'),
    path('api/room-list/create', chat.api.create_room_view, name='create-room'),
    path('api/bookbse/', include('BookBSE.api.urls')),
    path('api/food/', include('food.api.urls'))
]
