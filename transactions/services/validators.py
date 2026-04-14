from datetime import datetime
from decimal import Decimal, InvalidOperation
from transactions.services.exceptions import ETLValidationError

class TransactionRowValidator:
    @staticmethod
    def validate(row: dict, row_number: int) -> dict:
        required_fields = ["date", "product", "category", "amount"]
        for field in required_fields:
            if not row.get(field):
                raise ETLValidationError(f"Row {row_number}: {field} is required")

        try:
            parsed_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        except ValueError as exc:
            raise ETLValidationError(f"Row {row_number}: invalid date format, expected YYYY-MM-DD") from exc

        try:
            amount = Decimal(row["amount"])
        except (InvalidOperation, TypeError) as exc:
            raise ETLValidationError(f"Row {row_number}: amount must be numeric") from exc

        if amount < 0:
            raise ETLValidationError(f"Row {row_number}: amount cannot be negative")

        return {
            "date": parsed_date,
            "product": row["product"],
            "category": row["category"],
            "amount": amount,
        }
