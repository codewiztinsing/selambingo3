from django.test import TestCase
import factory
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import TelegramUser
from payments.models import Wallet, PaymentSession
from .models import Wallet, PaymentSession
import json

# To install factory-boy, run:
# pip install factory-boy


class TelegramUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TelegramUser
    
    telegram_id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f'user{n}')
    phone_number = factory.Sequence(lambda n: f'25191{n}123456')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = 'testpass123'

class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet
    
    user = factory.SubFactory(TelegramUserFactory)
    balance = 1000.0

class PaymentSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentSession
    
    user = factory.SubFactory(TelegramUserFactory)
    amount = 100.0
    session_id = factory.Sequence(lambda n: f'session_{n}')
    status = 'pending'

class PaymentViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = TelegramUserFactory()
        self.wallet = WalletFactory(user=self.user)
        
    def test_get_balance(self):
        url = f'/payments/balance/?user_id={self.user.telegram_id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['balance'], self.wallet.balance)

    def test_get_balance_invalid_user(self):
        url = '/payments/balance/?user_id=99999'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Wallet not found')

    def test_get_wallet(self):
        url = f'/payments/wallet/{self.user.telegram_id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['balance'], self.wallet.balance)

    def test_get_wallet_no_wallet(self):
        new_user = TelegramUserFactory()
        url = f'/payments/wallet/{new_user.telegram_id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['balance'], 0)

    def test_payment_success(self):
        session = PaymentSessionFactory(user=self.user)
        url = '/payments/success/'
        data = {'sessionId': session.session_id}
        
        response = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        updated_session = PaymentSession.objects.get(id=session.id)
        self.assertEqual(updated_session.status, 'success')

    def test_payment_success_invalid_session(self):
        url = '/payments/success/'
        data = {'sessionId': 'invalid_session'}
        
        response = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Payment session not found')

# Create your tests here.
