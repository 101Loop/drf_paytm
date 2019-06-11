from django.urls import path

from .views import ListAddTransactionRequestView
from .views import ListAddTransactionResponseView, PayNowTransaction


app_name = "drf_paytm"


urlpatterns = [
    path('request/', ListAddTransactionRequestView.as_view(),
         name="list-add-transaction-request"),
    path('response/', ListAddTransactionResponseView.as_view(),
         name="list-add-transaction-response"),
    path('now/', PayNowTransaction.as_view(),
         name="pay-now")
]
