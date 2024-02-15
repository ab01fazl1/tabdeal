from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import TransactionSerializer, AccountSerializer
from .models import Account, Transaction as Transaction_Model
from django.db import transaction
from django.db.models import F
from .exceptions import YouAreBadBakhtError, InvalidAccounts


class AccountView(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['get']


class TransactionView(ModelViewSet):
    
    queryset = Transaction_Model.objects.select_related()
    serializer_class = TransactionSerializer
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        data = serializer.data
        amount = data['amount']
        
        # create an atomic transaction
        with transaction.atomic():

            # get accounts and use select_for_update to lock them for the duration of the transaction
            from_account = Account.objects.select_for_update().get(data['from_account'])
            to_account = Account.objects.select_for_update().filter(phone_number=data['phone_number'])
            
            # dont allow someone to charge themselves
            if from_account == to_account:
                raise InvalidAccounts
            
            # create a transaction and check if balance will be more than 0 after the transaction
            if from_account.balance < amount:
                raise YouAreBadBakhtError
            else:
                Transaction_Model.objects.create(
                    account=from_account.id,
                    to_account=to_account.id,
                    amount=amount
                )
            
            # recalculate the balance
            from_account.update(balance=F('balance') - amount)
            to_account.update(balance=F('balance') + amount)

