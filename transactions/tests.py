from django.test import TestCase
from transactions.models import Transaction
from decimal import Decimal
from datetime import date

class TransactionModelTest(TestCase):
    def test_transaction_str(self):
        tx = Transaction.objects.create(
            date=date(2024, 1, 1),
            product="Milk",
            category="Food",
            amount=Decimal("10.00"),
            source_file="sample.csv",
        )
        self.assertIn("Milk", str(tx))
