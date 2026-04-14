from datetime import datetime
from django.http import Http404
from ninja import NinjaAPI, Query
from transactions.repositories.transaction_repository import TransactionRepository
from transactions.schemas import (
    HealthResponse,
    TransactionOut,
    ETLResponse,
    SummaryItem,
    DeleteResponse,
    ErrorResponse,
    FilterQuery,
)
from transactions.services.etl_service import ETLService
from transactions.services.summary_service import SummaryService

api = NinjaAPI(title="Advanced Budget ETL API", version="1.0.0")

repository = TransactionRepository()
etl_service = ETLService(repository=repository)

@api.get("/health", response=HealthResponse)
def health(request):
    return {
        "status": "ok",
        "service": "advanced-budget-etl-ninja-api",
        "timestamp": datetime.now(),
    }

@api.post("/etl/run", response={200: ETLResponse, 400: ErrorResponse})
def run_etl(request, file_path: str | None = None):
    result = etl_service.run(file_path=file_path)
    if result.inserted_rows == 0 and result.errors:
        return 400, {
            "detail": "ETL failed or no valid rows were inserted",
        }
    return {
        "message": "ETL completed successfully",
        "inserted_rows": result.inserted_rows,
        "skipped_rows": result.skipped_rows,
        "errors": result.errors,
    }

@api.get("/transactions", response=list[TransactionOut])
def list_transactions(request, filters: FilterQuery = Query(...)):
    return repository.filter_transactions(
        category=filters.category,
        product=filters.product,
    )

@api.get("/transactions/{transaction_id}", response={200: TransactionOut, 404: ErrorResponse})
def get_transaction(request, transaction_id: int):
    try:
        return repository.get_by_id(transaction_id)
    except Exception as exc:
        raise Http404("Transaction not found") from exc

@api.get("/summary/by-category", response=list[SummaryItem])
def summary_by_category(request):
    return list(SummaryService.by_category())

@api.delete("/transactions/clear", response=DeleteResponse)
def clear_transactions(request):
    deleted_rows = repository.delete_all()
    return {
        "message": "All transactions were deleted successfully",
        "deleted_rows": deleted_rows,
    }
