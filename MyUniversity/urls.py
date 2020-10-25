from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'MyUniversity'
urlpatterns = [
    path('users/', views.UsersList.as_view()),
]
