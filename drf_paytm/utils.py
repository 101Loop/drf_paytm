import base64
import string
import random
import hashlib

from Crypto.Cipher import AES

from django.core.validators import RegexValidator

IV = "@@@@&&&&####$$$$"
BLOCK_SIZE = 16


validate_order_id = RegexValidator(r'^[\w.-@]+$')
validate_customer_id = RegexValidator(r'^[\w@!_$.]+$')


def generate_parameters(attributes, cust_id):
    parameters = {
        'MID': str(str(attributes['mid'])),
        'INDUSTRY_TYPE_ID': str(attributes['itid']),
        'ORDER_ID': str(attributes['oid']),
        'WEBSITE': str(attributes['website']),
        'TXN_AMOUNT': str(round(attributes['amount'], 2)),
        'CHANNEL_ID': str(attributes['channel']),
        'CUST_ID': str(cust_id),
        'CALLBACK_URL': str(attributes['callback_url'])
    }
    if 'mobile' in attributes:
        parameters['MOBILE_NO'] = str(attributes['mobile'])
    if 'email' in attributes:
        parameters['EMAIL'] = str(attributes['email'])
    if 'payment_mode_only' in attributes:
        parameters['PAYMENT_MODE_ONLY'] = str(attributes['payment_mode_only'])
        parameters['AUTH_MODE'] = str(attributes['auth_mode'])
        parameters['PAYMENT_TYPE_ID'] = str(attributes['payment_type_id'])
        if 'bank_code' in attributes:
            parameters['BANK_CODE'] = str(attributes['bank_code'])
    return parameters


def generate_payment_page(param_dict):
    from .models import PayTMConfiguration

    pc = PayTMConfiguration.objects.get(mid=param_dict.get('MID'))

    html_code = """<html>
    <h1>%s<br><br>
        Merchant Check Out Page<br><br> 
        Please Do Not Refresh The Page
    </h1></br>
    <form method="post" action="%s" name="f1">
        <table border="1">
        <tbody> """ % (pc.company_name, pc.gateway_url)

    for key, value in param_dict.items():
        html_code += """
        <input type="hidden" name="%s" value="%s">""" % (key, value)
    html_code += """
        </tbody>
        </table>
        <script type="text/javascript">
            document.f1.submit();
        </script>
    </form>
</html>"""
    return html_code


def validate_key(value):
    from django.core.exceptions import ValidationError
    from django.utils.text import gettext_lazy as _
    if len(value) not in [16, 24, 32]:
        raise ValidationError(_("Merchant key must be of length 16, 24 or 32"))


def generate_checksum(param_dict, merchant_key, salt=None):
    print(param_dict)
    params_string = __get_param_string__(param_dict)
    salt = salt if salt else __id_generator__(4)
    final_string = '%s|%s' % (params_string, salt)

    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()

    hash_string += salt

    return __encode__(hash_string, IV, merchant_key)


def generate_refund_checksum(param_dict, merchant_key, salt=None):
    for i in param_dict:
        if "|" in param_dict[i]:
            param_dict = {}
            exit()
    params_string = __get_param_string__(param_dict)
    salt = salt if salt else __id_generator__(4)
    final_string = '%s|%s' % (params_string, salt)

    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()

    hash_string += salt

    return __encode__(hash_string, IV, merchant_key)


def generate_checksum_by_str(param_str, merchant_key, salt=None):
    params_string = param_str
    salt = salt if salt else __id_generator__(4)
    final_string = '%s|%s' % (params_string, salt)

    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()

    hash_string += salt

    return __encode__(hash_string, IV, merchant_key)


def verify_checksum(param_dict, merchant_key, checksum):
    # Remove checksum
    if 'CHECKSUMHASH' in param_dict:
        param_dict.pop('CHECKSUMHASH')

    # Get salt
    paytm_hash = __decode__(checksum, IV, merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum(param_dict, merchant_key,
                                            salt=salt)
    return calculated_checksum == checksum


def verify_checksum_by_str(param_str, merchant_key, checksum):
    # Remove checksum
    #if 'CHECKSUMHASH' in param_dict:
        #param_dict.pop('CHECKSUMHASH')

    # Get salt
    paytm_hash = __decode__(checksum, IV, merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum_by_str(param_str, merchant_key,
                                                   salt=salt)
    return calculated_checksum == checksum


def __id_generator__(size=6, chars=(string.ascii_uppercase + string.digits +
                                    string.ascii_lowercase)):
    return ''.join(random.choice(chars) for _ in range(size))


def __get_param_string__(params):
    params_string = []
    for key in sorted(params.keys()):
        if "REFUND" in params[key] or "|" in params[key]:
            respons_dict = {}
            exit()
        value = params[key]
        params_string.append('' if value == 'null' else str(value))
    return '|'.join(params_string)


def __pad__(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s)
                                                        % BLOCK_SIZE)


def __unpad__(s):
    return s[0:-ord(s[-1])]


def __encode__(to_encode, iv, key):
    # Pad
    to_encode = __pad__(to_encode)
    # Encrypt
    c = AES.new(key, AES.MODE_CBC, iv)
    to_encode = c.encrypt(to_encode)
    # Encode
    to_encode = base64.b64encode(to_encode)
    return to_encode.decode("UTF-8")


def __decode__(to_decode, iv, key):
    # Decode
    to_decode = base64.b64decode(to_decode)
    # Decrypt
    c = AES.new(key, AES.MODE_CBC, iv)
    to_decode = c.decrypt(to_decode)
    if type(to_decode) == bytes:
        # convert bytes array to str.
        to_decode = to_decode.decode()
    # remove pad
    return __unpad__(to_decode)
