from django.urls import path
from BookBSE.api import views

urlpatterns = [
    path('faculties/', views.Faculties.as_view()),
    path('fields/', views.Fields.as_view()),
    path('books/', views.Books.as_view()),
    path('stocks/', views.Stocks.as_view()),
    path('demands/', views.Demands.as_view()),
    path('trades/', views.Trades.as_view()),
    path('trades/history/', views.Histories.as_view()),
    path('trades/report/', views.ReportProblems.as_view()),
]