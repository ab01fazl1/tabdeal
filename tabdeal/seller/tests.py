from django.test import TestCase
from rest_framework.test import APIClient
from .models import Account, Transaction

import time

# a nice trick to create random phone numbers for my tests
def generate_random_phone_number():
    return str(hash(time.time()))[0:11]

class AccountTestCase(TestCase):

    def test_account_creation(self):
        self.acc = Account.objects.create(balance=100, phone_number=generate_random_phone_number())
        self.assertEqual(self.acc.balance, 100)

    def test_unique_phone_number(self):
        self.acc = Account.objects.create(balance=100, phone_number=generate_random_phone_number())
        self.assertRaises(Exception, Account.objects.create, balance=100, phone_number=self.acc.phone_number)

        
class TransactionTestCase(TestCase):
    transaction_url = 'http://127.0.0.1:90/api/v1/transactions/'

    def setUp(self):
        self.acc1 = Account.objects.create(balance=100, phone_number='00000000001')
        self.acc2 = Account.objects.create(balance=0, phone_number='11111111112')
    
    def test_successful_transaction(self):
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': 100,
            'from_account_id': self.acc1.id,
            'to_account_phone_number': '11111111112'
        }, format='json')
        self.assertEqual(cli.status_code, 201)

    def test_fail_negative_amount(self):
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': -10,
            'from_account_id': self.acc1.id,
            'to_account_phone_number': '11111111112'
        }, format='json')
        self.assertEqual(cli.status_code, 400)

    def test_fail_negative_balance(self):
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': 110,
            'from_account_id': self.acc1.id,
            'to_account_phone_number': '11111111112'
        }, format='json')
        self.assertEqual(cli.status_code, 400)

    def test_fail_account_invalid_pk(self):
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': 50,
            'from_account': self.acc1.id,
            'to_account': 'abc'
        }, format='json')
        self.assertEqual(cli.status_code, 400)

    def test_fail_same_accounts(self):
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': 50,
            'from_account_id': self.acc1.id,
            'to_account_phone_number': '00000000001'
        }, format='json')
        self.assertEqual(cli.status_code, 400)

    def test_fail_invalid_params(self):
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': None,
            'from_account_id': self.acc1.id,
            'to_account_phone_number': '11111111112'
        }, format='json')
        self.assertEqual(cli.status_code, 400)
        cli = client.post(self.transaction_url, {
            'amount': 110,
            'from_account_id': None,
            'to_account_phone_number': '11111111112'
        }, format='json')
        self.assertEqual(cli.status_code, 400)
        cli = client.post(self.transaction_url, {
            'amount': 110,
            'from_account_id': self.acc1.id,
            'to_account_phone_number': None
        }, format='json')
        self.assertEqual(cli.status_code, 400)