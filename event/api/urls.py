from django.urls import path
from event.api import views

urlpatterns = [
    path('admin/auth/all/', views.AdminAuthAll.as_view()),
    path('admin/auth/', views.AdminGetAuth.as_view()),
    path('admin/requests/all/', views.AdminAllRequests.as_view()),
    path('admin/requests/', views.AdminAcceptRequest.as_view()),
    path('admin/requests/history/', views.AdminRequestsHistory.as_view()),
    path('user/events/all/', views.get_all_events),
    path('user/event/', views.UserEvent.as_view()),
    path('user/event/history/', views.UserEventsHistory.as_view()),
]
