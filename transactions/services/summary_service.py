from django.db.models import Count, Sum
from transactions.models import Transaction

class SummaryService:
    @staticmethod
    def by_category():
        return (
            Transaction.objects.values("category")
            .annotate(
                total_amount=Sum("amount"),
                transaction_count=Count("id"),
            )
            .order_by("category")
        )
