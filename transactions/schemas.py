from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from ninja import Schema

class HealthResponse(Schema):
    status: str
    service: str
    timestamp: datetime

class TransactionOut(Schema):
    id: int
    date: date
    product: str
    category: str
    amount: Decimal
    source_file: str
    created_at: datetime

class ETLResponse(Schema):
    message: str
    inserted_rows: int
    skipped_rows: int
    errors: List[str]

class SummaryItem(Schema):
    category: str
    total_amount: Decimal
    transaction_count: int

class DeleteResponse(Schema):
    message: str
    deleted_rows: int

class ErrorResponse(Schema):
    detail: str

class FilterQuery(Schema):
    category: Optional[str] = None
    product: Optional[str] = None
