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

# from seller.command.setup_bank import bank_instance
# from .serializers import ChargeSerializer
# class ChargeView(ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = ChargeSerializer
#     http_method_names = ['post']
#     def perform_create(self, pk, serializer):
#         data = serializer.data
#         data['from_account_id'] = bank_instance.id
#         data['from_account_phone_number'] = Account.objects.get(pk=pk).phone_number
#         create_transaction(data)
# @api_view(['POST'])
# def charge_account(request, pk):
#     serializer = ChargeSerializer(data=request.data)
#     bank_obj = bank_instance
#     to_account_phone_number = Account.objects.get(pk=pk).phone_number
#     amount = request.data['amount']
#     data = {
#         'from_account_id': bank_obj.id,
#         'to_account_phone_number':to_account_phone_number,
#         'amount':amount,
#     }
#     create_transaction(data)
#     return Response(status=200)