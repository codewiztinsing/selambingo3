from typing import Any, TypeVar, Type, cast

T = TypeVar("T")

def from_float(x: Any) -> float:
    if not isinstance(x, (float, int)) or isinstance(x, bool):
        raise ValueError("Expected a float or int")
    return float(x)

def from_str(x: Any) -> str:
    if not isinstance(x, str):
        raise ValueError("Expected a string")
    return x

def to_float(x: Any) -> float:
    if not isinstance(x, (int, float)):
        raise ValueError("Expected an int or float")
    return float(x)

def to_class(c: Type[T], x: Any) -> dict:
    if not isinstance(x, c):
        raise ValueError(f"Expected instance of {c.__name__}")
    return cast(Any, x).to_dict()

class OrderDetail:
    def __init__(self, amount: float, description: str, items: str,
                 phone_number: str, telecom_operator: str, image: str) -> None:
        self.amount = amount
        self.description = description
        self.items = items
        self.phone_number = phone_number
        self.telecom_operator = telecom_operator
        self.image = image

    @staticmethod
    def from_dict(obj: Any) -> 'OrderDetail':
        if not isinstance(obj, dict):
            raise ValueError("Expected a dictionary")
        return OrderDetail(
            amount=from_float(obj.get("amount")),
            description=from_str(obj.get("description")),
            items=from_str(obj.get("items")),
            phone_number=from_str(obj.get("phoneNumber")),
            telecom_operator=from_str(obj.get("telecomOperator")),
            image=from_str(obj.get("image"))
        )

    def to_dict(self) -> dict:
        return {
            "amount": to_float(self.amount),
            "description": from_str(self.description),
            "items": from_str(self.items),
            "phoneNumber": from_str(self.phone_number),
            "telecomOperator": from_str(self.telecom_operator),
            "image": from_str(self.image)
        }

class Data:
    def __init__(self, redirect_url: str, cancel_url: str, success_url: str,
                 error_url: str, order_reason: str, currency: str, email: str,
                 first_name: str, last_name: str, nonce: str, order_detail: OrderDetail,
                 phone_number: str, session_expired: int, total_amount: str, tx_ref: str) -> None:
        self.redirect_url = redirect_url
        self.cancel_url = cancel_url
        self.success_url = success_url
        self.error_url = error_url
        self.order_reason = order_reason
        self.currency = currency
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.nonce = nonce
        self.order_detail = order_detail
        self.phone_number = phone_number
        self.session_expired = session_expired
        self.total_amount = total_amount
        self.tx_ref = tx_ref

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        if not isinstance(obj, dict):
            raise ValueError("Expected a dictionary")
        return Data(
            redirect_url=from_str(obj.get("redirect_url")),
            cancel_url=from_str(obj.get("cancel_url")),
            success_url=from_str(obj.get("success_url")),
            error_url=from_str(obj.get("error_url")),
            order_reason=from_str(obj.get("order_reason")),
            currency=from_str(obj.get("currency")),
            email=from_str(obj.get("email")),
            first_name=from_str(obj.get("first_name")),
            last_name=from_str(obj.get("last_name")),
            nonce=from_str(obj.get("nonce")),
            order_detail=OrderDetail.from_dict(obj.get("order_detail")),
            phone_number=from_str(obj.get("phone_number")),
            session_expired=int(from_str(obj.get("session_expired"))),
            total_amount=from_str(obj.get("total_amount")),
            tx_ref=from_str(obj.get("tx_ref"))
        )

    def to_dict(self) -> dict:
        return {
            "redirect_url": from_str(self.redirect_url),
            "cancel_url": from_str(self.cancel_url),
            "success_url": from_str(self.success_url),
            "error_url": from_str(self.error_url),
            "order_reason": from_str(self.order_reason),
            "currency": from_str(self.currency),
            "email": from_str(self.email),
            "first_name": from_str(self.first_name),
            "last_name": from_str(self.last_name),
            "nonce": from_str(self.nonce),
            "order_detail": to_class(OrderDetail, self.order_detail),
            "phone_number": from_str(self.phone_number),
            "session_expired": from_float(self.session_expired),
            "total_amount": from_str(self.total_amount),
            "tx_ref": from_str(self.tx_ref)
        }

class AddispayModel:
    def __init__(self, data: Data, message: str) -> None:
        self.data = data
        self.message = message

    @staticmethod
    def from_dict(obj: Any) -> 'AddispayModel':
        if not isinstance(obj, dict):
            raise ValueError("Expected a dictionary")
        return AddispayModel(
            data=Data.from_dict(obj.get("data")),
            message=from_str(obj.get("message"))
        )

    def to_dict(self) -> dict:
        return {
            "data": to_class(Data, self.data),
            "message": from_str(self.message)
        }

def addispay_model_from_dict(s: Any) -> AddispayModel:
    return AddispayModel.from_dict(s)

def addispay_model_to_dict(x: AddispayModel) -> Any:
    return to_class(AddispayModel, x)



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



