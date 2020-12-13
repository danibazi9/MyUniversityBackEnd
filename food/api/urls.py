from django.urls import path
from food.api import views

urlpatterns = [
    path('', views.Foods.as_view()),
    path('all/', views.get_all_foods),
    path('times/', views.Times.as_view()),
    path('admin/serve/', views.AdminServes.as_view()),
    path('admin/order/all/', views.AdminOrdersAll.as_view()),
    path('admin/order/', views.OrderFinished.as_view()),
    path('admin/serve/all/', views.AdminServesAll.as_view()),
    path('user/serve/', views.UserServes.as_view()),
    path('user/serve/all/', views.UserServesAll.as_view()),
    path('user/order/all/', views.OrdersAll.as_view()),
    path('user/order/add/', views.AddOrder.as_view()),
    path('user/order/edit/', views.EditOrder.as_view()),
    path('user/order/properties/', views.OrderProperties.as_view()),
    path('user/order/delete/', views.DeleteOrder.as_view()),
    path('user/order/history/', views.OrderHistory.as_view()),
]
