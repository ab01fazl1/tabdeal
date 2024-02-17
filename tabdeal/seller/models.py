from django.db import models


# instead of seller, I assume that everyone is an account
# and we do not allow a transaction between unregistered phone numbers
class Account(models.Model):

    balance = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=11, unique=True)
    
    def __str__(self):
         return f'user_id: {self.id},balance: {self.balance}'    


class Transaction(models.Model):

    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='outgoing_transactions')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ingoing_transactions')
    amount = models.PositiveIntegerField()


# singleton model to create one Bank instance
# class Bank(Account):

#     class Meta:
#         abstract = True
    
#     def save(self, *args, **kwargs):
#         self.pk = 1
#         super(Bank, self).save(*args, **kwargs)

#     @classmethod
#     def load(cls):
#             obj, created = cls.objects.get_or_create(pk=1)
#             return obj