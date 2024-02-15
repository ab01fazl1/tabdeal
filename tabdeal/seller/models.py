from django.db import models


# instead of seller, I assume that everyone is an account
# and we do not allow a transaction between unregistered phone numbers
class Account(models.Model):

    balance = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=11)
    
    def __str__(self):
         return f'user_id: {self.id},balance: {self.balance}'    


class Transaction(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_account')
    amount = models.IntegerField()


# singleton model to create one Bank instance
class SingletonModel(models.Model):

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
            obj, created = cls.objects.get_or_create(pk=1)
            return obj
    
# this is like money bank or storge or khazane 
class Bank(SingletonModel, Account):
    
    balance = models.IntegerField(default=1000000)