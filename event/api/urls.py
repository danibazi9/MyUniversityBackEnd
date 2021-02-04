from django.urls import path
from event.api import views

urlpatterns = [
    path('admin/auth/all/', views.AdminAuthAll.as_view()),
    path('admin/auth/', views.AdminAuth.as_view()),
    path('admin/requests/all/', views.get_all_requests),
    path('admin/requests/', views.Requests.as_view()),
    path('admin/requests/history/', views.AdminRequestsHistory.as_view()),
    path('user/all/', views.get_all_events),
    path('user/', views.UserEvent.as_view()),
    path('user/register/', views.UserRegisterEvent.as_view()),
    path('user/history/', views.UserEventsHistory.as_view()),
    path('user/culture-deputies/', views.get_all_deputies),
]
