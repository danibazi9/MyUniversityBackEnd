from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'MyUniversity'
urlpatterns = [
    path('api/users-list/', views.UsersList.as_view()),
    path('api/users-list/<int:stuID>', views.UsersDetails.as_view()),
    path('api/send-email/<int:stuID>', views.SendEmail.as_view()),
]
