"""
REST API based views for PayTM app
List Transaction Request
Add Transaction Request
List Transaction Response
Add Transaction Response

Author: Himanshu Shankar (https://himanshus.com)
"""

from drfaddons.generics import OwnerListCreateAPIView, OwnerRetrieveAPIView

from rest_framework.generics import CreateAPIView


class ListAddTransactionRequestView(OwnerListCreateAPIView):
    """
    GET: Provides a list of all Transaction Requests created by logged
    in user.

    POST: Creates a new PayTM Transaction Request in the system and
    provides front end with a checksum hash for sending to PayTM.

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from .serializers import TransactionRequestSerializer
    from .models import TransactionRequest

    serializer_class = TransactionRequestSerializer
    queryset = TransactionRequest.objects.all()


class RetrieveTransactionRequestView(OwnerRetrieveAPIView):
    """
    GET: Provides a list of all Transaction Requests created by logged
    in user.

    POST: Creates a new PayTM Transaction Request in the system and
    provides front end with a checksum hash for sending to PayTM.

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from .serializers import TransactionRequestSerializer
    from .models import TransactionRequest

    serializer_class = TransactionRequestSerializer
    queryset = TransactionRequest.objects.all()
    lookup_field = 'oid'


class AddTransactionResponseView(CreateAPIView):
    """
    GET: Provides a list of all Transaction Response created by logged
    in user.

    POST: Creates a Transaction Response record.

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from rest_framework.parsers import FormParser
    from rest_framework.permissions import AllowAny

    from .serializers import TransactionResponseSerializer
    from .models import TransactionResponse

    permission_classes = (AllowAny, )
    parser_classes = (FormParser, )
    serializer_class = TransactionResponseSerializer
    queryset = TransactionResponse.objects.all()

    def create(self, request, *args, **kwargs):
        from django.http import HttpResponseRedirect

        from rest_framework.response import Response
        from rest_framework import status

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if serializer.instance.t_request:
            return HttpResponseRedirect(
                serializer.instance.t_request.callback_url)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)


class PayNowTransaction(ListAddTransactionRequestView):
    from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
    from rest_framework.renderers import TemplateHTMLRenderer
    from rest_framework.parsers import FormParser, JSONParser

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer,
                        TemplateHTMLRenderer)
    parser_classes = (JSONParser, FormParser)

    def create(self, request, *args, **kwargs):
        from django.http.response import HttpResponse

        from rest_framework import status

        from .utils import generate_payment_page

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data

        if 'is_completed' in data:
            del data['is_completed']
        if 'id' in data:
            del data['id']
        if 'paytm_callback_url' in data:
            del data['paytm_callback_url']

        for attr in ['PAYMENT_MODE_ONLY', 'AUTH_MODE', 'PAYMENT_TYPE_ID',
                     'BANK_CODE', 'EMAIL', 'MOBILE_NO']:
            if attr in data and data[attr] is None:
                del data[attr]

        if 'serializer' in data:
            del data['serializer']

        return HttpResponse(generate_payment_page(param_dict=data),
                            status=status.HTTP_201_CREATED)
