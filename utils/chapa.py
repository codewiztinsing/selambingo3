import requests
from decouple import config
import hashlib

URL = "https://api.chapa.co/v1/transaction/"
CALLBACK_URL = "https://selambingo.pythonanywhere.com/home/"
headers_ = {
    "Authorization": f'Bearer {config("CHAPA_SECRET")}',
    "Content-type": "application/json",
}


class Chapa:
    @classmethod
    def initialize(self, amount, email, first_name, last_name, ref, **kwargs):
        request = requests.post(
            URL + "initialize",
            json={
                "amount": amount,
                "currency": "ETB",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "tx_ref": str(ref),
                "callback_url": CALLBACK_URL,
                "customization[title]": "Ashewa",
                "customization[description]": "It is time to pay",
            },
            headers=headers_,
        )
        return request.json()

    @classmethod
    def verify(self, tx):
        request = requests.get(f"{URL}verify/{tx}", headers=headers_)
        return request.json()

    @classmethod
    def get_hash(self):
        signer = hashlib.new("sha256")
        signer.update(config("CHAPA_WEBHOOK_SECRET").encode())
        return hashlib.sha256(config("CHAPA_WEBHOOK_SECRET").encode()).hexdigest()


