from django.db.models.signals import post_save

from django.dispatch import receiver

from drf_paytm.models import TransactionResponse
from drf_paytm.signals import payment_done


@receiver(signal=post_save, sender=TransactionResponse)
def transaction_response_handler(instance: TransactionResponse,
                                 sender, **kwargs):
    """
    Checks if payment has been completed successfully and hence, generates
    signal that developer is supposed to receive and do the needful.

    Parameters
    ----------
    instance: TransactionResponse
    kwargs: dict

    Returns
    -------
    """

    from drf_paytm.variables import SUCCESS
    if instance.status == SUCCESS:
        payment_done.send(sender=sender, instance=instance)
