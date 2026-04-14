from dataclasses import dataclass, field
from pathlib import Path
from django.conf import settings
from transactions.models import Transaction
from transactions.repositories.transaction_repository import TransactionRepository
from transactions.services.csv_reader import CSVReader
from transactions.services.validators import TransactionRowValidator
from transactions.services.exceptions import ETLValidationError, CSVFileNotFoundError

@dataclass
class ETLExecutionResult:
    inserted_rows: int = 0
    skipped_rows: int = 0
    errors: list[str] = field(default_factory=list)

class ETLService:
    def __init__(self, repository: TransactionRepository | None = None) -> None:
        self.repository = repository or TransactionRepository()

    def run(self, file_path: str | None = None) -> ETLExecutionResult:
        csv_path = file_path or settings.CSV_FILE_PATH
        source_file = Path(csv_path).name
        result = ETLExecutionResult()

        try:
            rows = CSVReader.read(csv_path)
        except CSVFileNotFoundError as exc:
            result.errors.append(str(exc))
            result.skipped_rows += 1
            return result

        valid_transactions = []
        for index, row in enumerate(rows, start=2):
            try:
                cleaned = TransactionRowValidator.validate(row, row_number=index)
                valid_transactions.append(
                    Transaction(source_file=source_file, **cleaned)
                )
            except ETLValidationError as exc:
                result.skipped_rows += 1
                result.errors.append(str(exc))

        if valid_transactions:
            created = self.repository.bulk_create(valid_transactions)
            result.inserted_rows = len(created)

        return result
