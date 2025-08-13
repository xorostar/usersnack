# Usersnack Challenge

A full-stack food ordering application built with FastAPI (backend) and React + TypeScript (frontend).

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
alembic upgrade head
python scripts/seed_db.py
uvicorn src.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run generate-sdk
npm run dev
```

## Architecture

- **Backend**: FastAPI with PostgreSQL, SQLAlchemy ORM, Alembic migrations
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, ShadCN UI
- **API**: RESTful endpoints with OpenAPI documentation
- **Database**: PostgreSQL with sample food data

## Features

- Browse food items with images and ingredients
- Add extras/toppings to orders
- Real-time price calculation
- Order APIs
- Responsive design
- Type-safe API communication

## Backend Details

### API Endpoints

- `GET /food-items` - List all food items
- `GET /food-items/{id}` - Get food item details
- `GET /extras` - List all extras (toppings, etc.)
- `POST /orders` - Create a new order
- `GET /docs` - Swagger Docs

### Backend Development

#### Running Tests

```bash
cd backend
pytest
```

#### Database Migrations

```bash
# Create new migration
alembic revision -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

#### Using SQLite (Development)

Edit `backend/database/core.py` and change `DATABASE_URL` to use SQLite:

```python
DATABASE_URL = "sqlite:///./test.db"
```

### Backend Environment Variables

| Variable          | Description                | Default                 |
| ----------------- | -------------------------- | ----------------------- |
| `DATABASE_URL`    | Database connection string | `postgresql://...`      |
| `SECRET_KEY`      | JWT secret key             | `your-secret-key`       |
| `ALLOWED_ORIGINS` | CORS origins               | `http://localhost:5173` |

## Frontend Details

### Features

- Browse food items with images and ingredients
- Add extras/toppings to orders
- Real-time price calculation
- Order history stored locally
- Responsive design with Tailwind CSS

### Frontend Development

#### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run generate-sdk` - Generate TypeScript SDK from backend API
- `npm run lint` - Run ESLint

#### Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── hooks/         # Custom React hooks
├── services/      # API service layer
├── sdk/           # Generated TypeScript SDK from OpenAPI Specs
└── types/         # TypeScript type definitions
```

### Frontend Environment Variables

| Variable           | Description     | Default                 |
| ------------------ | --------------- | ----------------------- |
| `VITE_BACKEND_URL` | Backend API URL | `http://localhost:8000` |

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Development Commands

- Backend tests: `cd backend && pytest`
- Frontend build: `cd frontend && npm run build`
- Generate SDK: `cd frontend && npm run generate-sdk`
