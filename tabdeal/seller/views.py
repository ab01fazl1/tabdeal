from rest_framework.viewsets import ModelViewSet
from .serializers import TransactionSerializer, AccountSerializer
from .models import Account, Transaction
from django.db.transaction import atomic
from django.db.models import F
from .exceptions import YouAreBadBakhtError, InvalidAccounts


class AccountView(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['get']


class TransactionView(ModelViewSet):
    
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        data = serializer.data
        amount = data['amount']
        
        # create an atomic transaction
        with atomic():

            # get accounts and use select_for_update to lock them for the duration of the transaction
            from_account = Account.objects.select_for_update().get(id=data['from_account_id'])
            to_account = Account.objects.select_for_update().get(phone_number=data['to_account_phone_number'])
            
            # dont allow someone to charge themselves
            if from_account == to_account:
                raise InvalidAccounts
            
            # create a transaction and check if balance will be more than 0 after the transaction
            if from_account.balance < amount:
                raise YouAreBadBakhtError
            else:
                Transaction.objects.create(
                    from_account=from_account,
                    to_account=to_account,
                    amount=amount
                )
            
            # recalculate the balance
            from_account.balance -= amount
            from_account.save()
            to_account.balance += amount
            to_account.save()

