from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Sum, Value, DecimalField
from django.db.models.functions import Coalesce



class WalletQuerySet(models.QuerySet):
    def annotate_balance(self):
        return self.annotate(
            balance=Coalesce(Sum("transactions__amount"), Value(0, output_field=DecimalField()))
        )


class Wallet(models.Model):
    label = models.CharField(max_length=255)

    objects = WalletQuerySet.as_manager()

    class Meta:
        indexes = [models.Index(fields=["label"])]
        ordering = ["id"]

    def __str__(self):
        balance = getattr(self, "balance", None)
        return f"{self.label} (Balance: {balance if balance is not None else 'N/A'})"


class Transaction(models.Model):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)

    class Meta:
        indexes = [
            models.Index(fields=["txid"]),
            models.Index(fields=["wallet"]),
        ]
        ordering = ["-id"]

    def __str__(self):
        return f"Transaction {self.txid} for {self.amount}"
