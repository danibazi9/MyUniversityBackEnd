from django.urls import path
from BookBSE.api import views

urlpatterns = [
    path('faculties/', views.Faculties.as_view()),
    path('fields/', views.Fields.as_view()),
]