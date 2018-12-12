"""
Functions related to PayTM API

Author: Himanshu Shankar (https://himanshus.com)
"""


def validate_transaction_status(orderid: str, status: str, txnid: str):
    """
    Gets transaction status and provides a True/False output

    Parameters
    ----------
    orderid: str | OrderID

    Returns
    -------
    bool
    """
    import requests

    from .models import PayTMConfiguration
    from .utils import generate_checksum

    try:
        pc: PayTMConfiguration = PayTMConfiguration.objects.get(is_active=True)
    except PayTMConfiguration.DoesNotExists:
        raise NotImplementedError("PayTM Configuration not found.")
    else:
        data = {'ORDERID': orderid, 'MID': pc.mid}
        data['CHECKSUMHASH'] = generate_checksum(param_dict=data,
                                                 merchant_key=pc.mkey)

        response = requests.post(url=pc.status_url, json=data)

        if 199 < response.status_code < 300:
            if (response.json().get("STATUS") == status
                    and response.json().get("TXNID") == txnid):
                return True

        return False
