from django.urls import path
from . import api

urlpatterns = [
    path('faculties', api.Faculties.as_view()),
    path('fields', api.Fields.as_view())
]