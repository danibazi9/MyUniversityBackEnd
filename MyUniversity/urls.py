from django.urls import path, include

import chat.api

app_name = 'MyUniversity'
urlpatterns = [
    path('api/chat/', include('chat.urls')),
    path('api/account/', include('account.api.urls', 'account_api')),
    path('api/room-list/', chat.api.chat_properties_view, name='chat'),
    path('api/room-list/create', chat.api.create_room_view, name='create-room'),
    path('api/bookbse/', include('BookBSE.api.urls')),
    path('api/food/', include('food.api.urls')),
    path('api/event/', include('event.api.urls'))
]
