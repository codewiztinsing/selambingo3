
from typing import Any, TypeVar, Type, cast

T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class OrderDetail:
    amount: float
    description: str
    items: str
    phone_number: str
    telecom_operator: str
    image: str

    def init(self, amount: float, description: str, items: str, phone_number: str, telecom_operator: str, image: str) -> None:
        self.amount = amount
        self.description = description
        self.items = items
        self.phone_number = phone_number
        self.telecom_operator = telecom_operator
        self.image = image

    @staticmethod
    def from_dict(obj: Any) -> 'OrderDetail':
        assert isinstance(obj, dict)
        amount = from_float(obj.get("amount"))
        description = from_str(obj.get("description"))
        items = from_str(obj.get("items"))
        phone_number = from_str(obj.get("phoneNumber"))
        telecom_operator = from_str(obj.get("telecomOperator"))
        image = from_str(obj.get("image"))
        return OrderDetail(amount, description, items, phone_number, telecom_operator, image)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = to_float(self.amount)
        result["description"] = from_str(self.description)
        result["items"] = from_str(self.items)
        result["phoneNumber"] = from_str(self.phone_number)
        result["telecomOperator"] = from_str(self.telecom_operator)
        result["image"] = from_str(self.image)
        return result


class Data:
    redirect_url: str
    cancel_url: str
    success_url: str
    error_url: str
    order_reason: str
    currency: str
    email: str
    first_name: str
    last_name: str
    nonce: str
    order_detail: OrderDetail
    phone_number: str
    session_expired: int
    total_amount: str
    tx_ref: str

    def init(self, redirect_url: str, cancel_url: str, success_url: str, error_url: str, order_reason: str, currency: str, email: str, first_name: str, last_name: str, nonce: str, order_detail: OrderDetail, phone_number: str, session_expired: int, total_amount: str, tx_ref: str) -> None:
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
        assert isinstance(obj, dict)
        redirect_url = from_str(obj.get("redirect_url"))
        cancel_url = from_str(obj.get("cancel_url"))
        success_url = from_str(obj.get("success_url"))
        error_url = from_str(obj.get("error_url"))
        order_reason = from_str(obj.get("order_reason"))
        currency = from_str(obj.get("currency"))
        email = from_str(obj.get("email"))
        first_name = from_str(obj.get("first_name"))
        last_name = from_str(obj.get("last_name"))
        nonce = from_str(obj.get("nonce"))
        order_detail = OrderDetail.from_dict(obj.get("order_detail"))
        phone_number = from_str(obj.get("phone_number"))
        session_expired = int(from_str(obj.get("session_expired")))
        total_amount = from_str(obj.get("total_amount"))
        tx_ref = from_str(obj.get("tx_ref"))
        return Data(redirect_url, cancel_url, success_url, error_url, order_reason, currency, email, first_name, last_name, nonce, order_detail, phone_number, session_expired, total_amount, tx_ref)

    def to_dict(self) -> dict:
        result: dict = {}
        result["redirect_url"] = from_str(self.redirect_url)
        result["cancel_url"] = from_str(self.cancel_url)
        result["success_url"] = from_str(self.success_url)
        result["error_url"] = from_str(self.error_url)
        result["order_reason"] = from_str(self.order_reason)
        result["currency"] = from_str(self.currency)
        result["email"] = from_str(self.email)
        result["first_name"] = from_str(self.first_name)
        result["last_name"] = from_str(self.last_name)
        result["nonce"] = from_str(self.nonce)
        result["order_detail"] = to_class(OrderDetail, self.order_detail)
        result["phone_number"] = from_str(self.phone_number)
        result["session_expired"] = from_str(str(self.session_expired))
        result["total_amount"] = from_str(self.total_amount)
        result["tx_ref"] = from_str(self.tx_ref)
        return result


class AddispayModel:
    data: Data
    message: str

    def init(self, data: Data, message: str) -> None:
        self.data = data
        self.message = message

    @staticmethod
    def from_dict(obj: Any) -> 'AddispayModel':
        assert isinstance(obj, dict)
        data = Data.from_dict(obj.get("data"))
        message = from_str(obj.get("message"))
        return AddispayModel(data, message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(Data, self.data)
        result["message"] = from_str(self.message)
        return result


def addispay_model_from_dict(s: Any) -> AddispayModel:
    return AddispayModel.from_dict(s)


def addispay_model_to_dict(x: AddispayModel) -> Any:
    return to_class(AddispayModel, x)
