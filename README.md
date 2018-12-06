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
- `ListAddTransactionResponseView`: All response data should be posted on this view. Doesn't requires a logged in user.
- `PayNowTransaction`: This view is for testing w/o a frontend client. It will open PayTM payment page.

### URLS
- `request/`: All payment request to be made via this URL.
- `response/`: All payment response to be posted on this URL.
- `now/`: For immediate testing of API, open this url.

### Quickstart Guide

- Complete `Installation Steps` (mentioned above)
- Create a configuration via `Django Admin` in `PayTM Configuration`
- Set `is_active` to `True`
- Note: Use sandbox mode credential at first
- Test API by accessing `/api/paytm/now/` endpoint
- Use `PayTM Testing Credential`:
```
Mobile: 7777777777
OTP: 489871
Password: Paytm12345
```
