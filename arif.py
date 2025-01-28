import requests
import uuid
api_key = "mx9dn1iRbrV9NrlbTb8WIzVbrLfpKtY6"

headers = {
    "x-arifpay-key":api_key
}

def generate_nonce():
    return str(uuid.uuid4())


body = {
    "cancelUrl": "https://api.selambingo.com/cancel",
    "phone":"251944294981",
    "email":"example@arifpay.net",
    "nonce": generate_nonce(),
    "errorUrl": "https://api.selambingo.com/error",
    "notifyUrl": "https://api.selambingo.com/notify",
    "successUrl": "https://api.selambingo.com/success",
    "paymentMethods": ["TELEBIRR","AWASH","AWASH_WALLET","PSS","CBE","AMOLE","BOA","KACHA","TELEBIRR_USSD","HELLOCASH","MPESSA"],
    "expireDate": "2025-02-01T03:45:27",
    "items": [
        {
            "name": "Name",
            "quantity": 1,
            "price": 1,
            "description": "Item description ",
            "image": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        }
    ],
    "beneficiaries": [
        {
            "accountNumber": "01320811436100",
            "bank": "AWINETAA",
            "amount": 1
        }
    ],
    "lang": "EN"
}


checkout_url = "https://gateway.arifpay.org/api/checkout/session"

response = requests.post(url=checkout_url, headers=headers, json=body)

print(response.json().get("data").get("paymentUrl"))