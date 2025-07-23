from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction as db_transaction
from django.db.models import Sum

from apps.wallets.models import Transaction, Wallet


def get_actual_balance(wallet: Wallet) -> Decimal:
    return wallet.transactions.aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0")


def create_transaction(*, wallet: Wallet, txid: str, amount: Decimal) -> Transaction:
    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)

        current_balance = get_actual_balance(wallet)
        new_balance = current_balance + amount

        if new_balance < 0:
            raise ValidationError("Transaction would result in negative wallet balance")

        return Transaction.objects.create(wallet=wallet, txid=txid, amount=amount)


def update_transaction(*, instance: Transaction, amount: Decimal) -> Transaction:
    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=instance.wallet.pk)

        current_balance = get_actual_balance(wallet)
        current_balance -= instance.amount

        new_balance = current_balance + amount

        if new_balance < 0:
            raise ValidationError("Transaction update would result in negative wallet balance")

        instance.amount = amount
        instance.save(update_fields=["amount"])
        return instance


def delete_transaction(*, instance: Transaction):
    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=instance.wallet.pk)

        current_balance = get_actual_balance(wallet)
        new_balance = current_balance - instance.amount

        if new_balance < 0:
            raise ValidationError("Cannot delete transaction: wallet balance would become negative")

        instance.delete()
