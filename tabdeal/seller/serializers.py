from rest_framework import serializers
from seller.models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # i dont recommend fields=all, but for the sake of quicker development i chose this
        fields = '__all__'


class TransactionSerializer(serializers.Serializer):
    from_account_id = serializers.IntegerField()
    to_account_phone_number = serializers.CharField(max_length=100)
    # now we avoid getting negative amounts
    amount = serializers.IntegerField(min_value=0, required=True)