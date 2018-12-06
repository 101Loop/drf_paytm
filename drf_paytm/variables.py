from django.utils.text import gettext_lazy as _


SUCCESS = "TXN_SUCCESS"
FAILED = "TXN_FAILURE"
PENDING = "PENDING"
STATUS_CHOICES = (
    (SUCCESS, 'Success'),
    (FAILED, 'Failed'),
    (PENDING, 'Pending'),
)
CREDIT_CARD = "CC"
DEBIT_CARD = "DC"
NET_BANKING = "NB"
UPI = "UPI"
PAYTM_WALLET = "PPI"
MODE_CHOICES = (
    (CREDIT_CARD, _("Credit Card")),
    (DEBIT_CARD, _("Debit Card")),
    (NET_BANKING, _("Net Banking")),
    (UPI, _("UPI")),
    (PAYTM_WALLET, _("PayTM Wallet"))
)

WEB = 'WEB'
WAP = 'WAP'
CHANNEL_CHOICES = (
    (WEB, _("Website")),
    (WAP, _("Mobile Website/App")),
)

CARD = '3D'
WALLET_NETBANKING = 'USRPWD'
AUTH_MODE_CHOICES = (
    (CARD, _("Credit/Debit Card")),
    (WALLET_NETBANKING, _("Wallet/Net Banking"))
)
