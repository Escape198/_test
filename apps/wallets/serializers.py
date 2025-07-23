from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from rest_framework_json_api import serializers

from apps.wallets.models import Transaction, Wallet
from apps.wallets.services import create_transaction, update_transaction


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "label", "balance"]
        resource_name = "wallets"

    def get_balance(self, obj):
        return obj.transactions.aggregate(total=models.Sum("amount"))["total"] or 0


class TransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.ResourceRelatedField(queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = ["id", "wallet", "txid", "amount"]
        resource_name = "transactions"

    def validate(self, data):
        amount = data.get("amount", getattr(self.instance, "amount", None))
        wallet = data.get("wallet", getattr(self.instance, "wallet", None))

        if wallet and amount is not None:
            total = wallet.transactions.aggregate(total=Sum("amount"))["total"] or 0
            current_balance = total

            if self.instance:
                current_balance -= self.instance.amount

            new_balance = current_balance + amount

            if new_balance < 0:
                raise ValidationError("Transaction would result in negative wallet balance")

        return data

    def create(self, validated_data):
        return create_transaction(**validated_data)

    def update(self, instance, validated_data):
        amount = validated_data.get("amount", instance.amount)
        return update_transaction(instance=instance, amount=amount)
