from django.urls import path
from event.api import views

urlpatterns = [
    path('all/', views.get_all_events),
    path('add/', views.AddEvent.as_view()),
    path('properties/', views.EventProperties.as_view()),
    path('edit/', views.EditEvent.as_view()),
    path('delete/', views.RemoveEvent.as_view()),
    path('history/', views.EventHistory.as_view()),
]
