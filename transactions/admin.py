from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "product", "category", "amount", "source_file", "created_at")
    search_fields = ("product", "category", "source_file")
    list_filter = ("category", "date")
