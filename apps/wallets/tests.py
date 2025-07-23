import json
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient

from apps.wallets.models import Transaction, Wallet


class WalletTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wallet = Wallet.objects.create(label="Test Wallet", balance=100.0)

    def test_create_wallet(self):
        response = self.client.post(
            "/api/wallets/",
            {
                "data": {
                    "type": "wallets",
                    "attributes": {"label": "New Wallet", "balance": "50.0"},
                }
            },
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 201)

    def test_negative_balance(self):
        wallet = Wallet(label="Invalid Wallet", balance=-10)
        with self.assertRaises(ValidationError):
            wallet.save()

    def test_wallet_balance_ignored_on_create(self):
        response = self.client.post(
            "/api/wallets/",
            {
                "data": {
                    "type": "wallets",
                    "attributes": {"label": "Invalid Wallet", "balance": "99999999.0"},
                }
            },
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 201)
        wallet_id = response.data["data"]["id"]
        created = Wallet.objects.get(id=wallet_id)
        self.assertEqual(created.balance, Decimal("0"))


class TransactionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wallet = Wallet.objects.create(label="Test Wallet", balance=100.0)

    def test_create_transaction(self):
        response = self.client.post(
            "/api/transactions/",
            {
                "data": {
                    "type": "transactions",
                    "attributes": {
                        "txid": "tx123",
                        "amount": "50.0",
                    },
                    "relationships": {
                        "wallet": {
                            "data": {"type": "wallets", "id": str(self.wallet.id)}
                        }
                    },
                }
            },
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 201)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("150.0"))

    def test_negative_balance_transaction(self):
        response = self.client.post(
            "/api/transactions/",
            {
                "data": {
                    "type": "transactions",
                    "attributes": {
                        "txid": "tx124",
                        "amount": "-200.0",
                    },
                    "relationships": {
                        "wallet": {
                            "data": {"type": "wallets", "id": str(self.wallet.id)}
                        }
                    },
                }
            },
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_transaction(self):
        tx = Transaction.objects.create(
            wallet=self.wallet, txid="tx125", amount=Decimal("10.0")
        )
        response = self.client.patch(
            f"/api/transactions/{tx.id}/",
            {
                "data": {
                    "type": "transactions",
                    "id": str(tx.id),
                    "attributes": {"amount": "30.0"},
                }
            },
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 200)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("120.0"))

    def test_delete_transaction(self):
        tx = Transaction.objects.create(
            wallet=self.wallet, txid="tx126", amount=Decimal("20.0")
        )
        response = self.client.delete(f"/api/transactions/{tx.id}/")
        self.assertEqual(response.status_code, 204)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("80.0"))
