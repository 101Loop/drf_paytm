# PayTM | Django REST Framework

**A package for PayTM integration in Django REST Framework**<br>

`PayTM | Django REST Framework` is a Django packaged app that provides necessary `views` based in Django REST Framework.
It enables easy integration of PayTM Payment Gateway with Web/Mobile Application with a RESTful API based server.

Contributors: **WE'RE LOOKING FOR SOMEONE WHO CAN CONTRIBUTE IN DOCS**
- **[Civil Machines Technologies Private Limited](https://github.com/civilmahines)**: For providing me platform and
funds for research work. This project is hosted currently with `CMT` only. 
- **[Himanshu Shankar](https://github.com/iamhssingh)**: Himanshu Shankar has initiated this project and worked on this
project to collect useful functions and classes that are being used in various projects.

#### Installation

- Download and Install via `pip`
```
pip install drf_paytm
```
or<br>
Download and Install via `easy_install`
```
easy_install drf_paytm
```
- Add, if wanted, `drfaddons` in `INSTALLED_APPS` (This is although not required!)
```
INSTALLED_APPS = [
    ...
    'drf_paytm',
    ...
]
```
- Also add other dependencies in `INSTALLED_APPS`<br>
```
INSTALLED_APPS = [
    ...
    'drfaddons',
    ...
]
```
- Include urls of `drf_paytm` in `urls.py`
```
urlpatterns = [
    ...
    path('api/paytm/', include('drf_paytm.urls')),
    ...
]

# or

urlpatterns = [
    ...
    url(r'^api/paytm/', include('drf_paytm.urls')),
    ...
]
```
- Run migrate command:
```
python manage.py migrate
```

### Frontend API Integration Guideline
1. Prepare `json` data to post on `request/` view: `{"oid": "ORDER_ID", "amount": "200", "callback_url": "FRONT_END APP URL"}`
2. `callback_url`: FrontEnd URL to open when payment is successful. Must not have any queryset as `?oid=ORDER_ID` is 
appended.
3. Post to `request/` and parse response to prepare a HTML form as per code shown below.
4. Don't add `<input>` for empty and `null` fields from json response of `request/` API.
5. Set `CALLBACK_URL` in HTML from `paytm_callback_url` of JSON.
6. Once the payment is done, user is redirected to `response/` view which will verify payment.
7. If payment is verified by Django Backend, user is redirected to `http://callback_url?oid=ORDER_ID`.
8. Access `order/ORDER_ID/` API to get `is_completed` status. If it's `false`, check `last_payment_status`.

**Note: In case of critical failure, server's JSON response is shown.**

Sample HTML Code to be generated by FrontEnd App(from PayTM)
```
<html>
    <head>
        <title>Merchant Check Out Page</title>
    </head>
    <body>
        <center><h1>Please do not refresh this page...</h1></center>
        <form method="post" action="https://securegw-stage.paytm.in/theia/processTransaction" name="f1">
            <table border="1">
                <tbody>
                    <input type="hidden" name="MID" value="rxazcv89315285244163">
                    <input type="hidden" name="WEBSITE" value="WEBSTAGING">
                    <input type="hidden" name="ORDER_ID" value="order1">
                    <input type="hidden" name="CUST_ID" value="cust123">
                    <input type="hidden" name="MOBILE_NO" value="7777777777">
                    <input type="hidden" name="EMAIL" value="username@emailprovider.com">
                    <input type="hidden" name="INDUSTRY_TYPE_ID" value="Retail">
                    <input type="hidden" name="CHANNEL_ID" value="WEB">
                    <input type="hidden" name="TXN_AMOUNT" value="100.12">
                    <input type="hidden" name="CALLBACK_URL" value="https://Merchant_Response_URL>">
                    <input type="hidden" name="CHECKSUMHASH" value="ZWdMJOr1yGiFh1nns2U8sDC9VzgUDHVnQpG
                    pVnHyrrPb6bthwro1Z8AREUKdUR/K46x3XvFs6Xv7EnoSOLZT29qbZJKXXvyEuEWQIJGkw=">
                </tbody>
            </table>
        <script type="text/javascript">
            document.f1.submit();
        </script>
        </form>
    </body>
</html>
```

### MODELS
The application has three models:

- `PayTMConfiguration`: You need to define your PayTM configurations in this model. Only one object can have
`is_active` set to `True` which will be used with PayTM API.
- `TransactionRequest`: This will contain all the PayTM Transaction Request that one will create with PayTM.
- `TransactionResponse`: This will contain all the responses received from PayTM API against transaction.

### VIEWS
The application has following views:

- `ListAddTransactionRequestView`: All payment request should be made on this view. Requires a logged in user.
It'll provide user with required data, including `checksum hash` that will be used with PayTM API.
- `AddTransactionResponseView`: Response from PayTM is posted on this view. URL for this view should go as 
`CALLBACK_URL`. This view then redirects user to FrontEnd app with `OID` as queryset parameter.
- `PayNowTransaction`: This view is for testing w/o a frontend client. It will open PayTM payment page.

### URLS
- `request/`: All payment request to be made via this URL.
- `response/`: All response from PayTM is posted on this URL.
- `order/OID/`: Retrieve specific payment request data.
- `now/`: For immediate testing of API, open this url.

### Quickstart Guide

- Complete `Installation Steps` (mentioned above)
- Create a configuration via `Django Admin` in `PayTM Configuration`.
- Provide `base_url` of your Backend Server.
- Set `is_active` to `True`
- Note: Use sandbox mode credential at first
- Test API by accessing `/api/paytm/now/` endpoint
- Use `PayTM Testing Credential`:
```
Mobile: 7777777777
OTP: 489871
Password: Paytm12345
```
