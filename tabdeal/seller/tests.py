from django.test import TestCase
from rest_framework.test import APIClient
from .models import Account, Transaction, Bank


class FunctionalityTestCase(TestCase):
    transaction_url = 'http://127.0.0.1:8000/api/v1/transactions/'
    charge_url = 'http://127.0.0.1:8000/api/v1/charge/'

    def setUp(self):
        self.bank = Bank.objects.create(balance=10000)
        self.acc1 = Account.objects.create()
        self.acc2 = Account.objects.create()

    def test(self):
        client = APIClient()

        # charge both accounts 10 times
        for _ in range(10):
            cli = client.post(self.charge_url, {
                'amount': 110,
                'to_account_id': self.acc1.id,
            }, format='json')

            self.assertEqual(cli.status_code, 201)

        # charge account 2 10times
            cli = client.post(self.charge_url, {
                'amount': 110,
                'to_account_id': self.acc2.id,
            }, format='json')

            self.assertEqual(cli.status_code, 201)

        # check if accounts are charged properly
        self.acc1.refresh_from_db()
        self.acc2.refresh_from_db()
        self.bank.refresh_from_db()
        self.assertEqual(self.acc1.balance, 1100)
        self.assertEqual(self.acc2.balance, 1100)
        self.assertEqual(self.bank.balance, 7800)


        # sell 1000 charges from account 1 and account 2
        for _ in range(1000):

            # acc 1 sell charge 
            cli = client.post(self.transaction_url, {
                'amount': 1,
                'from_account_id': self.acc1.id,
                'phone_number': '11111111112'
            }, format='json')

            self.assertEqual(cli.status_code, 201)
            
            # acc 2 sell charge 
            cli = client.post(self.transaction_url, {
                'amount': 1,
                'from_account_id': self.acc2.id,
                'phone_number': '11111111112'
            }, format='json')

            self.assertEqual(cli.status_code, 201)

        # check if accounts have the proper balance
        self.acc1.refresh_from_db()
        self.acc2.refresh_from_db()
        self.assertEqual(self.acc1.balance, 100)
        self.assertEqual(self.acc2.balance, 100)

'''    

# class ChargeTestCase(TestCase):

class TransactionTestCase(TestCase):
    transaction_url = 'http://127.0.0.1:90/api/v1/transactions/'
    charge_url = 'http://127.0.0.1:90/api/v1/charge/'

    def setUp(self):
        self.bank = Bank.objects.create(balance=1000)
        self.acc1 = Account.objects.create()
        self.acc2 = Account.objects.create()
    
    def test_successful_charge(self):
        # a sample successful charge
        client = APIClient()
        
        # call a post api
        cli = client.post(self.charge_url, {
            'amount': 100,
            'to_account_id': self.acc1.id,
        }, format='json')
        
        # refresh account
        self.acc1.refresh_from_db()
        
        # test if acc balance and bank balance changed
        self.assertEqual(self.acc1.balance, 100)
        self.assertEqual(self.bank.balance, 900)
        self.assertEqual(cli.status_code, 201)

    def test_successful_transaction(self):
        
        # a sample successful transaction
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': 100,
            'from_account_id': self.acc1.id,
            'phone_number': '11111111112'
        }, format='json')

        self.acc1.refresh_from_db()
        self.assertEqual(self.acc1.balance, 0)
        self.assertEqual(cli.status_code, 201)

    def test_fail_negative_amount(self):
        # test invalid (negative) transfer amount
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': -10,
            'from_account_id': self.acc1.id,
            'phone_number': '11111111112'
        }, format='json')

        self.assertEqual(self.acc1.balance)
        self.assertEqual(cli.status_code, 400)

    def test_fail_negative_balance(self):
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': 110,
            'from_account_id': self.acc1.id,
            'phone_number': '11111111112'
        }, format='json')
        self.assertEqual(cli.status_code, 400)

    def test_fail_account_invalid_pk(self):
        # request to an invalid account
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': 50,
            'from_account': self.acc1.id,
            'to_phone_number': 'abc'
        }, format='json')
        self.assertEqual(cli.status_code, 400)

    def test_fail_same_accounts(self):
        # same accounts in a call -> 400 error
        client = APIClient()
        cli = client.post(self.transaction_url, {
            'amount': 50,
            'from_account_id': self.acc1.id,
            'phone_number': '00000000001'
        }, format='json')
        self.assertEqual(cli.status_code, 400)

    def test_fail_invalid_params(self):
        # test for false parameters
        client = APIClient()

        cli = client.post(self.transaction_url, {
            'amount': None,
            'from_account_id': self.acc1.id,
            'phone_number': '11111111112'
        }, format='json')
        self.assertEqual(cli.status_code, 400)

        cli = client.post(self.transaction_url, {
            'amount': 110,
            'from_account_id': None,
            'phone_number': '11111111112'
        }, format='json')
        self.assertEqual(cli.status_code, 400)

        cli = client.post(self.transaction_url, {
            'amount': 110,
            'from_account_id': self.acc1.id,
            'phone_number': None
        }, format='json')
        self.assertEqual(cli.status_code, 400)
'''