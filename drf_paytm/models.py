"""
Models for PayTM App:
1. PayTM Configuration
2. Transaction Request
3. Transaction Response

Author: Himanshu Shankar (https://himanshus.com)
"""

from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class PayTMConfiguration(CreateUpdateModel):
    """
    Contains PayTM Configurations. Only one object can have is_active
    set to True that will be used by the system by default.
    Currently to provision for multiple configuration at the runtime.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .utils import validate_key

    mid = models.CharField(verbose_name=_("Merchant ID"), max_length=20,
                           unique=True)
    mkey = models.CharField(verbose_name=_("Merchant Key"), max_length=32,
                            validators=[validate_key])
    is_active = models.BooleanField(verbose_name=_("Is Active?"),
                                    default=False)
    gateway_url = models.URLField(verbose_name=_("Payment Gateway URL"),
                                  default="https://securegw-stage.paytm.in/the"
                                          "ia/processTransaction")
    status_url = models.URLField(verbose_name=_("Payment Status URL"),
                                 default="https://securegw-stage.paytm.in/merc"
                                         "hant-status/getTxnStatus")
    company_name = models.CharField(verbose_name=_("Company Name"),
                                    max_length=254)

    def __str__(self):
        return self.mid

    def clean_fields(self, exclude=None):
        """
        Used to validate the value of is_active
        Parameters
        ----------
        exclude: list of fields that is to be excluded while checking

        Returns
        -------
        None

        Raises
        ------
        ValidationError: for is_active field.

        Author: Himanshu Shankar (https://himanshus.com)
        """
        from django.core.exceptions import ValidationError

        if 'is_active' not in exclude:
            try:
                pc = PayTMConfiguration.objects.get(is_active=True)
            except PayTMConfiguration.DoesNotExist:
                pass
            except PayTMConfiguration.MultipleObjectsReturned:
                raise ValidationError({'is_active':
                                           _("Multiple configuration is "
                                             "active. Keep only 1 "
                                             "configuration active at a "
                                             "time.")})
            else:
                if pc.mid is not self.mid:
                    raise ValidationError({'is_active': _("Another "
                                                          "configuration is "
                                                          "active. Deactivate "
                                                          "it first.")})
        super(PayTMConfiguration, self).clean_fields(exclude=exclude)

    class Meta:
        verbose_name = _("PayTM Configuration")
        verbose_name_plural = _("PayTM Configurations")


class TransactionRequest(CreateUpdateModel):
    """
    Contains all Transaction Request that are made.

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from .utils import validate_key, validate_order_id
    from .variables import CHANNEL_CHOICES, MODE_CHOICES, AUTH_MODE_CHOICES

    mid = models.CharField(verbose_name=_("Merchant ID"), max_length=20)
    itid = models.CharField(verbose_name=_("Industry Type ID"), max_length=20)
    oid = models.CharField(verbose_name=_("Order ID"), max_length=50,
                           unique=True, validators=[validate_order_id])
    website = models.CharField(verbose_name=_("Website"), max_length=30)
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=15,
                                 decimal_places=3)
    channel = models.CharField(verbose_name=_("Channel"), max_length=3,
                               choices=CHANNEL_CHOICES)
    checksum = models.CharField(verbose_name=_("Checksum"), max_length=108)
    mobile = models.CharField(verbose_name=_("Customer's Mobile Number"),
                              max_length=15, null=True, blank=True)
    email = models.EmailField(verbose_name=_("Customer's Email"),
                              max_length=254, null=True, blank=True)
    callback_url = models.URLField(verbose_name=_("Callback URL"),
                                   max_length=255)
    payment_mode_only = models.CharField(verbose_name=_("Payment Mode "
                                                        "Only"),
                                         max_length=3, null=True, blank=True)

    # Following are conditional i.e. only required if payment mode is set
    auth_mode = models.CharField(verbose_name=_("Auth Mode"), max_length=10,
                                 null=True, blank=True,
                                 choices=AUTH_MODE_CHOICES,
                                 help_text=_("Required If PAYMENT_MODE_ONLY "
                                             "= YES, then For Credit/Debit "
                                             "card - 3D For Wallet, "
                                             "Net Banking – USRPWD"))
    payment_type_id = models.CharField(verbose_name=_("Payment Type ID"),
                                       null=True, blank=True, max_length=15,
                                       choices=MODE_CHOICES,
                                       help_text=_("Required If "
                                                   "PAYMENT_MODE_ONLY = Yes "
                                                   "| CC/DC/NB/UPI/PPI/EMI"))
    bank_code = models.CharField(verbose_name=_("Bank Code"), null=True,
                                 blank=True, max_length=5,
                                 help_text=_("Required If PAYMENT_MODE_ONLY "
                                             "= Yes PAYMENT_TYPE_ID = NB "))
    mkey = models.CharField(verbose_name=_("Merchant Key"),
                            validators=[validate_key], max_length=32)

    @property
    def cid(self):
        """
        Provides Customer ID as per the user ID.
        Returns
        -------
        int: self.created_by.id

        Author: Himanshu Shankar (https://himanshus.com)
        """
        return self.created_by.id

    def completed(self):
        """
        Checks if the Transaction Request has been completed and the
        transaction has been made successfully by the end user.
        Returns
        -------
        bool: True if any of TransactionResponse with same OrderID(oid)
        has status set to TXN_SUCCESS, False otherwise.

        Author: Himanshu Shankar (https://himanshus.com)
        """
        from .variables import SUCCESS

        if TransactionResponse.objects.filter(oid=self.oid,
                                              status=SUCCESS).count() > 0:
            return True
        return False
    completed.short_description = _("Is Completed?")
    is_completed = property(completed)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        from .utils import generate_checksum
        parameters = {
            'MID': str(self.mid),
            'INDUSTRY_TYPE_ID': str(self.itid),
            'ORDER_ID': str(self.oid),
            'WEBSITE': str(self.website),
            'TXN_AMOUNT': str(round(self.amount, 2)),
            'CHANNEL_ID': str(self.channel),
            'CUST_ID': str(self.created_by.id),
            'CALLBACK_URL': str(self.callback_url)
        }
        if self.mobile:
            parameters['MOBILE_NO'] = str(self.mobile)
        if self.email:
            parameters['EMAIL'] = str(self.email)
        if self.payment_mode_only:
            parameters['PAYMENT_MODE_ONLY'] = str(self.payment_mode_only)
            parameters['AUTH_MODE'] = str(self.auth_mode)
            parameters['PAYMENT_TYPE_ID'] = str(self.payment_type_id)
            if self.bank_code:
                parameters['BANK_CODE'] = str(self.bank_code)
        self.checksum = generate_checksum(param_dict=parameters,
                                          merchant_key=self.mkey)
        super(TransactionRequest, self).save(force_insert=force_insert,
                                             force_update=force_update,
                                             using=using,
                                             update_fields=update_fields)

    def __str__(self):
        return self.oid

    class Meta:
        verbose_name = _("Transaction Request")
        verbose_name_plural = _("Transaction Requests")


class TransactionResponse(models.Model):
    """
    Contains all Transaction Responses. Serializer provides a check
    from TransactionRequest with the help of OrderID(oid).

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from .variables import STATUS_CHOICES, MODE_CHOICES

    mid = models.CharField(verbose_name=_("Merchant ID"), max_length=20)
    tid = models.CharField(verbose_name=_("Transaction ID"), max_length=64,
                           null=True, blank=True)
    cid = models.CharField(verbose_name=_("Customer ID"), max_length=64,
                           null=True, blank=True)
    oid = models.CharField(verbose_name=_("Order ID"), max_length=50)
    bnkid = models.TextField(verbose_name=_("Bank Transaction ID"),
                             null=True, blank=True)
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=15,
                                 decimal_places=3)
    currency = models.CharField(verbose_name=_("Currency"), max_length=3,
                                default=_("INR"))
    status = models.CharField(verbose_name=_("Status"), max_length=20,
                              choices=STATUS_CHOICES)
    code = models.CharField(verbose_name=_("Response Code"),
                            max_length=10)
    message = models.CharField(verbose_name=_("Response Message"),
                               max_length=500)
    timestamp = models.DateTimeField(verbose_name=_("Transaction Date Time"),
                                     null=True, blank=True)
    gateway = models.CharField(verbose_name=_("Gateway"), max_length=15,
                               null=True, blank=True)
    bank = models.CharField(verbose_name=_("Bank Name"), max_length=500,
                            null=True, blank=True)
    mode = models.CharField(verbose_name=_("Mode of Payment"), max_length=15,
                            choices=MODE_CHOICES, null=True, blank=True)
    checksum = models.CharField(verbose_name=_("Checksum Hash"),
                                max_length=108)
    bin_number = models.CharField(
        verbose_name=_("Starting 6 Digit Number of Card"), max_length=6,
        null=True, blank=True)
    card_last_num = models.CharField(verbose_name=_("Last 4 digit of Card"),
                                     max_length=4, null=True, blank=True)
    raw_response = models.TextField(verbose_name=_("Raw Response"))
    t_request = models.ForeignKey(to=TransactionRequest,
                                  on_delete=models.PROTECT,
                                  verbose_name=_("Transaction Request"),
                                  null=True, blank=True)

    def __str__(self):
        return self.oid

    class Meta:
        verbose_name = _("Transaction Response")
        verbose_name_plural = _("Transaction Responses")
