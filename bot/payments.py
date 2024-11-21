import requests
import random
import string

apiKey="DEFAULT_af37ed09-7a87-4d0a-92d4-822ac4eb3642"
				
headers = {
   "Auth":apiKey
}


def generate_nonce(length=64):
    characters = string.ascii_letters + string.digits + string.punctuation
    nonce = ''.join(random.choice(characters) for _ in range(length))
    return nonce




data = {
       "redirect_url": "http://example.com/redirect",
        "cancel_url": "https://eg.app.goo.gl/cancel",
        "success_url": "http://eg.app.goo.gl/callback",
        "error_url": "https://eg.app.goo.gl/error",
        "order_reason": "1 Ferrari La'Ferrari Roadster",
        "currency": "ETB",
        "email": "dawit@dawit.com",
        "first_name": "Dawit",
        "last_name": "Elias",
        "nonce":  "selam_pay_" + generate_nonce(64),
        "order_detail": {
            "amount": 1.01,
            "description": "this is the t-shirt I ordered",
            "items": "1 Ferrari La'Ferrari Roadster",
            "phoneNumber": "0921309013",
            "telecomOperator": "ethio_telecom",
            "image": "https://images.app.goo.gl/pYmev5W8J5AXpBin7"
        },
        "phone_number": "+251921309013",
        "session_expired": "5000",
        "total_amount": "1.01",
        "tx_ref": "selam_pay_" + generate_nonce(64),
       
        
}  


payload = {
   "data":data,
   "message":"test message"
}


import json

def make_request(payload,addispay_checkout_api_url):
   response = requests.post(addispay_checkout_api_url,json=payload ,headers=headers) #json=json.dumps(payload,indent=4), )

  #  print("data to api = ",payload)
   print("response = ",response.text)
   if response.status_code ==200:
     response_content = response.json()
     return response_content["checkout_url"] + "/" + response_content["uuid"]
   return False
addispay_checkout_api_url="https://uat.api.addispay.et/checkout-api/v1/create-order"

print(make_request(payload,addispay_checkout_api_url))

 