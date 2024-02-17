from rest_framework.viewsets import ModelViewSet
from .serializers import TransactionSerializer, AccountSerializer
from .models import Account, Transaction
from .services import create_transaction

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
        create_transaction(data)
        
