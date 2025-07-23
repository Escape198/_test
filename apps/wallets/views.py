from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_json_api.views import AutoPrefetchMixin

from apps.wallets.filters import TransactionFilter, WalletFilter
from apps.wallets.models import Transaction, Wallet
from apps.wallets.serializers import TransactionSerializer, WalletSerializer
from apps.wallets.services import delete_transaction


class WalletViewSet(AutoPrefetchMixin, ModelViewSet):
    queryset = Wallet.objects.annotate_balance().order_by("id")
    serializer_class = WalletSerializer

    filterset_class = WalletFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    ordering_fields = ["id", "label", "balance"]

    prefetch_for_includes = {
        "transactions": ["transactions"],
    }


class TransactionViewSet(AutoPrefetchMixin, ModelViewSet):
    queryset = Transaction.objects.select_related("wallet").all()
    serializer_class = TransactionSerializer

    filterset_class = TransactionFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    ordering_fields = ["id", "txid", "amount"]

    prefetch_for_includes = {
        "wallet": ["wallet"],
    }

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_transaction(instance=instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
