from rest_framework.viewsets import ModelViewSet
from .serializers import SellTransactionSerializer, AccountSerializer, ChargeTransactionSerializer
from .models import Account, Transaction
from .services import create_transaction, create_charge_transaction

class AccountView(ModelViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['post', 'get']

class TransactionView(ModelViewSet):
    
    queryset = Transaction.objects.all()
    serializer_class = SellTransactionSerializer
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        data = serializer.data
        create_transaction(data)
        
class ChargeView(ModelViewSet):

    queryset = Transaction.objects.all()
    serializer_class = ChargeTransactionSerializer
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        data = serializer.data
        create_charge_transaction(data)
