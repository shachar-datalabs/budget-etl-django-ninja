from django.db import models

class Transaction(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source_file = models.CharField(max_length=255, default="unknown.csv")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "id"]

    def __str__(self) -> str:
        return f"{self.date} | {self.product} | {self.category} | {self.amount}"
