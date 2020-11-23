from django.urls import path
from food.api import views

urlpatterns = [
    path('', views.Foods.as_view()),
    path('all/', views.get_all_foods),
    path('serve/', views.Serves.as_view()),
    path('serve/all/', views.ServesAll.as_view()),
]
