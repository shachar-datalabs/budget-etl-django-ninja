from typing import Iterable
from django.db.models import QuerySet
from transactions.models import Transaction

class TransactionRepository:
    @staticmethod
    def get_all() -> QuerySet[Transaction]:
        return Transaction.objects.all()

    @staticmethod
    def filter_transactions(category: str | None = None, product: str | None = None) -> QuerySet[Transaction]:
        queryset = Transaction.objects.all()
        if category:
            queryset = queryset.filter(category__iexact=category)
        if product:
            queryset = queryset.filter(product__icontains=product)
        return queryset

    @staticmethod
    def get_by_id(transaction_id: int) -> Transaction:
        return Transaction.objects.get(id=transaction_id)

    @staticmethod
    def bulk_create(transactions: Iterable[Transaction]) -> list[Transaction]:
        return Transaction.objects.bulk_create(list(transactions))

    @staticmethod
    def delete_all() -> int:
        deleted_count, _ = Transaction.objects.all().delete()
        return deleted_count
