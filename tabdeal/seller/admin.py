from django.contrib import admin
from .models import Account, Transaction, Bank


class BankAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'balance'
    )

class AccountAdmin(admin.ModelAdmin):
    # Accounts admin custom class
    list_display = (
        'id',
        'balance',
    )

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'from_account',
        'to_account',
        'amount',
    )

admin.site.register(Bank, BankAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)