from django.db.transaction import atomic
from .exceptions import InsufficientFunds, InvalidAccounts
from .models import Account, Transaction, Bank
from django.db.models import F


def create_transaction(data):
    amount = data['amount']
    # create an atomic transaction
    with atomic():

        # get accounts and use select_for_update to lock them for the duration of the transaction
        try:
            from_account_queryset = Account.objects.select_for_update().filter(id=data['from_account_id'])
            phone_number = data['phone_number']
        except Account.DoesNotExist:
            raise InvalidAccounts
        
        # create a transaction and check if balance will be more than 0 after the transaction
        from_account_obj = from_account_queryset[0]
        if from_account_obj.balance < amount:
            raise InsufficientFunds
        else:
            Transaction.objects.create(
                from_account=from_account_obj,
                amount=amount,
                phone_number=phone_number,
            )
        
        # recalculate the balance
        from_account_queryset.update(balance=F('balance') - amount)

def create_charge_transaction(data):
    
     amount = data['amount']
     
     with atomic():
            # from bank to seller account
            try:
                # change this logic later
                bank = Bank.objects.select_for_update().first()
                to_account = Account.objects.select_for_update().get(pk=data['to_account_id'])
            except Account.DoesNotExist:
                raise InvalidAccounts
            
            # bank cannot charge itself
            if bank == to_account:
                raise InvalidAccounts

            # create a transaction and check if balance will be more than 0 after the transaction
            if bank.balance < amount:
                raise InsufficientFunds
            
            # direction incoming for easier queries
            else:
                Transaction.objects.create(
                    direction=Transaction.DirectionType.INCOMING,
                    from_account=bank,
                    to_account=to_account,
                    amount=amount
                )
            
            # recalculate the balance
            bank.balance -= amount
            bank.save()

            # optional: i could put a save point here
            
            to_account.balance += amount
            to_account.save()