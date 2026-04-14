# Advanced Budget ETL - Django Ninja API

פרויקט Budget ETL מתקדם עם:
- Django + Django Ninja API
- PostgreSQL
- Docker + Docker Compose
- ETL לטעינת CSV
- שכבת Services ו-Repositories
- ולידציה, טיפול בשגיאות וסטטיסטיקות
- Swagger Docs מובנה דרך Django Ninja

## פורטים
- API: `8001`
- PostgreSQL: `5433`

הפורט של Postgres שונה מ-5432 כדי למנוע התנגשות עם Postgres אחר שכבר רץ על המחשב.

## מבנה הפרויקט
- `config/` - הגדרות Django
- `transactions/` - מודול הדומיין
- `transactions/services/` - לוגיקת ETL
- `transactions/repositories/` - גישה לנתונים
- `data/` - קובץ CSV לדוגמה

## הרצה עם Docker
1. העתק את `.env.example` ל-`.env`
2. הרץ:
   ```bash
   docker compose up --build
   ```
3. פתח:
   - API root: `http://localhost:8001/api/`
   - Swagger docs: `http://localhost:8001/api/docs`

## Endpoints עיקריים
- `GET /api/health`
- `POST /api/etl/run`
- `GET /api/transactions`
- `GET /api/transactions/{id}`
- `GET /api/summary/by-category`
- `DELETE /api/transactions/clear`

## דוגמת הרצת ETL
```bash
curl -X POST http://localhost:8001/api/etl/run
```

או עם קובץ מותאם:
```bash
curl -X POST "http://localhost:8001/api/etl/run?file_path=/app/data/sample_transactions.csv"
```

## דוגמת תשובה
```json
{
  "message": "ETL completed successfully",
  "inserted_rows": 12,
  "skipped_rows": 2,
  "errors": [
    "Row 7: amount must be numeric",
    "Row 13: date is required"
  ]
}
```

## הרצה מקומית בלי Docker
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
## API Endpoints

- GET /api/health
- POST /api/etl/run
- GET /api/transactions

  ## How it works

1. CSV file is loaded from data folder
2. ETL process parses and validates data
3. Data is stored in PostgreSQL
4. API exposes endpoints for querying data

## הערות
- אפשר להחליף את קובץ ה-CSV בקלות.
- אפשר להרחיב את המודל לעמודות נוספות.
- הפרויקט מוכן טוב לראיונות, תרגול OOP, API, ETL ו-Docker.
