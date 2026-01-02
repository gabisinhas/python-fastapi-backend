# Python FastAPI Project

This project is a backend API built with [FastAPI](https://fastapi.tiangolo.com/), SQLAlchemy, and Alembic, designed for managing products and suppliers.

## Features

- CRUD for Products
- CRUD for Suppliers
- Pagination and ordering for suppliers
- Relationship between products and suppliers
- Automatic API documentation via Swagger at `/docs`

## Project Structure

```
.
├── app.py                # FastAPI application entry point
├── alembic/              # Database migrations
├── database/             # Database config, models, session
├── repository/           # Data access repositories
├── routes/               # API routes (products and suppliers)
├── schemas/              # Pydantic schemas for validation
├── services/             # Business logic
├── pyproject.toml        # Project dependencies and metadata
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-fastapi-project
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set the `DATABASE_URL` environment variable in a `.env` file:
   ```
   DATABASE_URL=sqlite:///./test.db
   # or your preferred connection string
   ```

5. Run database migrations:
   ```
   alembic upgrade head
   ```

## Running the Application

```
uvicorn app:app --reload
```

Access the interactive documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

- Products: `/products`
- Suppliers: `/suppliers`

## License

MIT
