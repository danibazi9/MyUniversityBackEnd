from django.urls import path
from event.api import views

urlpatterns = [
    path('admin/auth/all/', views.AdminAuthAll.as_view()),
    path('admin/auth/', views.AdminAuth.as_view()),
    path('admin/requests/all/', views.AdminAllRequests.as_view()),
    path('admin/requests/', views.AdminAcceptRequest.as_view()),
    path('admin/requests/history/', views.AdminRequestsHistory.as_view()),
    path('user/all/', views.get_all_events),
    path('user/', views.UserEvent.as_view()),
    path('user/history/', views.UserEventsHistory.as_view()),
]
