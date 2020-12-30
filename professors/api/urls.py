from django.urls import path
from professors.api import views

urlpatterns = [
    path('admin/', views.AdminProfessor.as_view()),
    path('user/all/', views.get_all_professors),
    path('user/', views.UserGetProfessor.as_view()),
    path('times/', views.get_all_times),
    path('faculty/', views.get_all_faculties),
    path('research-axes/', views.get_research_axes),
]
