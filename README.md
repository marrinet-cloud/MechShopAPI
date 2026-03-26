# Mechanic Shop API (Flask + SQLAlchemy + Marshmallow)

Factory-pattern Flask API for a small mechanic shop (Customers, Mechanics, Service Tickets).

## Setup

### 1) Create & activate a virtual environment

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Create a MySQL database
In MySQL Workbench:
```sql
CREATE DATABASE mechanic_shop_db;
```

### 4) Configure DB connection
Edit `config.py` and replace:
- `<YOUR MYSQL PASSWORD>`
- `<YOUR DATABASE>` (example: `mechanic_shop_db`)

### 5) Run
```bash
python app.py
```

Server:
- http://127.0.0.1:5000/

## Endpoints

### Customers
- POST `/customers/`
- GET `/customers/`
- PUT `/customers/<id>`
- DELETE `/customers/<id>`

### Mechanics
- POST `/mechanics/`
- GET `/mechanics/`
- PUT `/mechanics/<id>`
- DELETE `/mechanics/<id>`

### Service Tickets
- POST `/service-tickets/`
- PUT `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>`
- PUT `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>`
- GET `/service-tickets/`

## Postman
Import: `postman/Mechanic_Shop_API.postman_collection.json`  
Set variable `baseUrl` to `http://127.0.0.1:5000`.
