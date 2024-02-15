from django.contrib import admin
from .models import Account, Transaction


class AccountAdmin(admin.ModelAdmin):
    # Accounts admin custom class
    list_display = (
        'id',
        'balance',
    )
    search_fields = ('id', 'currency',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'account',
        'to_account',
        'amount',
    )


admin.site.register(Account, AccountAdmin, Transaction, TransactionAdmin)
