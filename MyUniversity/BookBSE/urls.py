from django.urls import path
from . import api

urlpatterns = [
    path('faculties', api.Faculties.as_view()),
    path('fields/<int:facultyID>', api.Fields.as_view()),
    path('book/', api.Books.as_view()),
    # path('book/fid=<int:fieldID>', api.Books.as_view()),
]