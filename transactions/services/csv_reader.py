from pathlib import Path
import csv
from transactions.services.exceptions import CSVFileNotFoundError

class CSVReader:
    REQUIRED_COLUMNS = {"date", "product", "category", "amount"}

    @staticmethod
    def read(file_path: str) -> list[dict]:
        path = Path(file_path)
        if not path.exists():
            raise CSVFileNotFoundError(f"CSV file not found: {file_path}")

        with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            if not reader.fieldnames:
                raise CSVFileNotFoundError("CSV file is empty or missing header row")

            normalized_headers = {header.strip().lower() for header in reader.fieldnames if header}
            missing_columns = CSVReader.REQUIRED_COLUMNS - normalized_headers
            if missing_columns:
                raise CSVFileNotFoundError(
                    f"Missing required columns: {', '.join(sorted(missing_columns))}"
                )

            rows = []
            for row in reader:
                normalized_row = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k}
                rows.append(normalized_row)
            return rows
