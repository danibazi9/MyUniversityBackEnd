from django.urls import path
from BookBSE.api import views

urlpatterns = [
    path('faculties/', views.get_all_faculties),
    path('fields/', views.Fields.as_view()),
    path('books/', views.Books.as_view()),
    path('stocks/', views.Stocks.as_view()),
    path('stocks/history/', views.StocksHistory.as_view()),
    path('demands/', views.Demands.as_view()),
    path('demands/accept/', views.DemandAcceptor.as_view()),
    path('trades/', views.Trades.as_view()),
    path('trades/history/', views.TradesHistory.as_view()),
    path('trades/report/', views.ReportProblems.as_view()),
]
