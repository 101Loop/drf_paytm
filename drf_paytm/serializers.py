"""
Serializers for PayTM app
They also map regular model field name to PayTM based keys.

Author: Himanshu Shankar (https://himanshus.com)
"""
from rest_framework import serializers

from django.utils.text import gettext_lazy as _


class TransactionRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction Request.
    Effectively maps regular model fields to PayTM based keys.

    Can also be used to get PayTM based parameter dictionary from model
    object as the keys in PayTM and field name in model are different.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .variables import CHANNEL_CHOICES, MODE_CHOICES, AUTH_MODE_CHOICES

    MID = serializers.CharField(source='mid', read_only=True)
    INDUSTRY_TYPE_ID = serializers.CharField(source='itid', read_only=True)
    ORDER_ID = serializers.CharField(source='oid', read_only=True)
    WEBSITE = serializers.CharField(source='website', read_only=True)
    TXN_AMOUNT = serializers.DecimalField(source='amount', read_only=True,
                                          max_digits=10, decimal_places=2)
    CHANNEL_ID = serializers.ChoiceField(source='channel', default='WEB',
                                         choices=CHANNEL_CHOICES,
                                         read_only=True)
    CALLBACK_URL = serializers.CharField(source='callback_url', read_only=True)
    CUST_ID = serializers.CharField(source='cid', read_only=True)
    MOBILE_NO = serializers.CharField(source='mobile', read_only=True)
    EMAIL = serializers.CharField(source='email', read_only=True)
    PAYMENT_MODE_ONLY = serializers.CharField(source='payment_mode_only',
                                              read_only=True)
    AUTH_MODE = serializers.ChoiceField(source='auth_mode', read_only=True,
                                        choices=AUTH_MODE_CHOICES)
    PAYMENT_TYPE_ID = serializers.ChoiceField(source='payment_type_id',
                                              read_only=True,
                                              choices=MODE_CHOICES)
    BANK_CODE = serializers.CharField(source='bank_code', read_only=True)
    CHECKSUMHASH = serializers.CharField(source='checksum', read_only=True)

    def validate(self, attrs: dict)->dict:
        """
        Checks for following:
        AUTH_MODE & PAYMENT_TYPE_ID is set if PAYMENT_MODE_ONLY is set.
        BANK_CODE is set if PAYMENT_TYPE_ID is for Net Banking.

        Also adds mid, checksum and mkey to the request for saving in
        model.
        Parameters
        ----------
        attrs: dict of attributes sent by client.

        Returns
        -------
        dict: attrs

        Author: Himanshu Shankar (https://himanshus.com)
        """

        from .models import PayTMConfiguration
        from .variables import NET_BANKING

        from rest_framework.exceptions import APIException

        if 'PAYMENT_MODE_ONLY' in attrs:
            if 'AUTH_MODE' not in attrs:
                raise serializers.ValidationError(_("If Payment Mode Only is "
                                                    "set, providing AUTH_MODE "
                                                    "is compulsory."))
            if 'PAYMENT_TYPE_ID' not in attrs:
                raise serializers.ValidationError(_("If Payment Mode Only is "
                                                    "set, providing "
                                                    "PAYMENT_TYPE_ID is "
                                                    "compulsory."))
            elif (attrs.get('PAYMENT_TYPE_ID') is NET_BANKING
                  and 'BANK_CODE' not in attrs):
                raise serializers.ValidationError(
                    _("If Payment Mode Only is  set and Payment Type is  "
                      "Net banking, providing BANK_CODE is compulsory."))
        try:
            paytm_config = PayTMConfiguration.objects.get(is_active=True)
        except PayTMConfiguration.DoesNotExist:
            raise APIException(detail=_("Server has not configured a PayTM "
                                        "Configuration yet."))
        except PayTMConfiguration.MultipleObjectsReturned:
            raise APIException(detail=_("Improper PayTM Configuration found. "
                                        "Server has multiple active PayTM "
                                        "configurations."))
        else:
            attrs['mid'] = paytm_config.mid
            attrs['mkey'] = paytm_config.mkey
        return attrs

    class Meta:
        from .models import TransactionRequest

        model = TransactionRequest
        fields = ('id', 'MID', 'INDUSTRY_TYPE_ID', 'CUST_ID', 'ORDER_ID',
                  'WEBSITE', 'TXN_AMOUNT', 'CHANNEL_ID', 'MOBILE_NO',
                  'EMAIL', 'CALLBACK_URL', 'PAYMENT_MODE_ONLY', 'AUTH_MODE',
                  'PAYMENT_TYPE_ID', 'BANK_CODE', 'CHECKSUMHASH',

                  'itid', 'oid', 'website', 'amount', 'channel', 'bank_code',
                  'mobile', 'email', 'callback_url', 'payment_mode_only',
                  'auth_mode', 'payment_type_id')
        read_only_fields = ('id', 'CHECKSUMHASH', 'is_completed', 'MID',
                            'INDUSTRY_TYPE_ID', 'CUST_ID', 'ORDER_ID',
                            'WEBSITE', 'TXN_AMOUNT', 'CHANNEL_ID',
                            'MOBILE_NO', 'EMAIL', 'CALLBACK_URL',
                            'PAYMENT_MODE_ONLY', 'AUTH_MODE',
                            'PAYMENT_TYPE_ID', 'BANK_CODE', 'CHECKSUMHASH')
        extra_kwargs = {
            key: {'write_only': True} for key in
            set(fields) - set(read_only_fields)
        }


class TransactionResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction Response.
    Effectively maps regular model fields to PayTM based keys.

    Can also be used to get PayTM based parameter dictionary from model
    object as the keys in PayTM and field name in model are different.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .variables import STATUS_CHOICES

    MID = serializers.CharField(source='mid')
    TXNID = serializers.CharField(source='tid', required=False)
    ORDERID = serializers.CharField(source='oid')
    CUST_ID = serializers.CharField(source='cid', required=False)
    BANKTXNID = serializers.CharField(source='bnkid', allow_blank=True)
    TXNAMOUNT = serializers.CharField(source='amount')
    CURRENCY = serializers.CharField(source='currency', default='INR')
    STATUS = serializers.ChoiceField(source='status', choices=STATUS_CHOICES)
    RESPCODE = serializers.CharField(source='code')
    RESPMSG = serializers.CharField(source='message')
    TXNDATE = serializers.CharField(source='timestamp', required=False)
    GATEWAYNAME = serializers.CharField(source='gateway', required=False)
    BANKNAME = serializers.CharField(source='bank', required=False)
    PAYMENTMODE = serializers.CharField(source='mode', required=False)
    CHECKSUMHASH = serializers.CharField(source='checksum')
    BIN_NUMBER = serializers.CharField(source='bin_number', required=False)
    CARD_LAST_NUMS = serializers.CharField(source='card_last_num', required=False)

    def validate_MID(self, value):
        """
        Checks if Merchant ID is present in system.

        Parameters
        ----------
        value: str | merchant ID

        Returns
        -------
        str: merchant ID

        Author: Himanshu Shankar (https://himanshus.com)
        """

        from .models import PayTMConfiguration

        try:
            PayTMConfiguration.objects.get(mid=value)
        except PayTMConfiguration.DoesNotExist:
            raise serializers.ValidationError(_("Provided Merchant ID does "
                                                "not exists in the system."))
        return value

    def validate_ORDERID(self, value):
        """
        Checks if Order ID is present in system.

        Parameters
        ----------
        value: str | order ID

        Returns
        -------
        str: order ID

        Author: Himanshu Shankar (https://himanshus.com)
        """

        from .models import TransactionRequest

        try:
            TransactionRequest.objects.get(oid=value)
        except TransactionRequest.DoesNotExist:
            raise serializers.ValidationError(_("No PayTM Transaction "
                                                "request with provided order "
                                                "ID exists in the system."))
        return value

    def validate(self, attrs):
        """
        Verifies the checksum hash sent by client.
        Also adds raw_response and t_request to the attributes.

        Parameters
        ----------
        attrs: dict | attributes

        Returns
        -------
        dict: attributes

        Author: Himanshu Shankar (https://himanshus.com)
        """

        import json

        from .utils import verify_checksum
        from .models import PayTMConfiguration, TransactionRequest

        try:
            pc = PayTMConfiguration.objects.get(mid=attrs.get('MID'))
        except PayTMConfiguration.DoesNotExist:
            pc = None
            # raise serializers.ValidationError(_("Provided merchant ID does "
            #                                     "not exists in the system."))
        else:
            if not verify_checksum(param_dict=attrs, merchant_key=pc.mkey,
                                   checksum=attrs.get('CHECKSUMHASH')):
                raise serializers.ValidationError(_("Could not verify "
                                                    "transaction response."))
        attrs['raw_response'] = json.dumps(self.context.get('request').data)
        attrs['t_request'] = TransactionRequest.objects.get(oid=
                                                            attrs.get('oid'))
        return attrs

    class Meta:
        from .models import TransactionResponse

        model = TransactionResponse
        fields = ('id', 'MID', 'TXNID', 'ORDERID', 'CUST_ID', 'BANKTXNID',
                  'TXNAMOUNT', 'CURRENCY', 'STATUS', 'RESPCODE', 'RESPMSG',
                  'TXNDATE', 'GATEWAYNAME', 'BANKNAME', 'PAYMENTMODE',
                  'CHECKSUMHASH', 'BIN_NUMBER', 'CARD_LAST_NUMS')
