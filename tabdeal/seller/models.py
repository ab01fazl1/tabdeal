from django.db import models

# instead of seller, I assume that everyone is an account
# and we do not allow a transaction between unregistered phone numbers
class Account(models.Model):

    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    def __str__(self):
         return f'user_id: {self.id}, balance: {self.balance}'    

class Bank(Account):
    pass

# this transaction model can both handle charges from bank and outgoing charges
class Transaction(models.Model):
    class DirectionType(models.TextChoices):
        INCOMING = 'incoming'
        OUTGOING = 'outgoing'

    direction = models.CharField(max_length=9, choices=DirectionType)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='outgoing_transactions')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='incoming_transactions', null=True, blank=True)
    phone_number = models.CharField(max_length=11)  # phone number of the receiver of the transaction
    amount = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)