from django.urls import path

from . import views

app_name = "drf_paytm"


urlpatterns = [
    path('request/', views.ListAddTransactionRequestView.as_view(),
         name="list-add-transaction-request"),
    path('order/<oid>/', views.RetrieveTransactionRequestView.as_view(),
         name="retrieve-transaction-request"),
    path('response/', views.AddTransactionResponseView.as_view(),
         name="list-add-transaction-response"),
    path('now/', views.PayNowTransaction.as_view(),
         name="pay-now")
]
