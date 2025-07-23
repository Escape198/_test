import django_filters

from apps.wallets.models import Transaction, Wallet


class TransactionFilter(django_filters.FilterSet):
    amount_min = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    wallet = django_filters.NumberFilter(field_name="wallet_id")

    class Meta:
        model = Transaction
        fields = ["wallet", "txid", "amount_min", "amount_max"]


class WalletFilter(django_filters.FilterSet):
    label = django_filters.CharFilter(field_name="label", lookup_expr="icontains")

    class Meta:
        model = Wallet
        fields = ["label"]
