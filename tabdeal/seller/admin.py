from django.contrib import admin
from .models import Account, Transaction


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


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)