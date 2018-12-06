from django.urls import path

from .views import ListAddTransactionRequestView
from .views import ListAddTransactionResponseView, PayNowTransaction


app_name = "drf_paytm"


urlpatterns = [
    path('request/', ListAddTransactionRequestView.as_view(),
         name="List Add Transaction Request"),
    path('response/', ListAddTransactionResponseView.as_view(),
         name="List-Add-Transaction-Response"),
    path('now/', PayNowTransaction.as_view(),
         name="Pay Now")
]
