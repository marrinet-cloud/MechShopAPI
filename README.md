# 🔧 Mechanic Shop API

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-API-black)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange)
![JWT](https://img.shields.io/badge/Auth-JWT-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License](https://img.shields.io/badge/License-Student_Project-lightgrey)

---

## 📌 Overview

A full-featured REST API built with **Flask** for managing a mechanic shop system, including:

- Customers 👤
- Mechanics 🛠️
- Service Tickets 🎟️
- Inventory 📦

This project demonstrates **authentication, authorization, caching, rate limiting, and advanced database relationships**.

---

## ✨ Features

### 🔐 Authentication & Authorization

- JWT authentication using `python-jose`
- Role-based access:
  - 👤 Customer
  - 🛠️ Mechanic
  - 👑 Admin
- Protected routes using decorators

---

### ⚡ Performance & Security

- Rate limiting with Flask-Limiter
- Caching with Flask-Caching
- Password hashing with Werkzeug

---

### 🧠 Advanced Functionality

- Many-to-many relationships:
  - Tickets ↔ Mechanics
  - Tickets ↔ Inventory
- Advanced query (batch updates):
  - Add/remove mechanics in one request
- Pagination for customers

---

## 🧱 Tech Stack

| Category      | Tech              |
| ------------- | ----------------- |
| Backend       | Flask             |
| Database      | MySQL             |
| ORM           | SQLAlchemy        |
| Serialization | Marshmallow       |
| Auth          | JWT (python-jose) |
| Caching       | Flask-Caching     |
| Rate Limiting | Flask-Limiter     |

---

## 📁 Project Structure

mechanic_shop_api/
│
├── app/
│ ├── blueprints/
│ │ ├── customers/
│ │ ├── mechanics/
│ │ ├── service_tickets/
│ │ ├── inventory/
│ ├── models.py
│ ├── extensions.py
│ ├── auth.py
│ └── init.py
│
├── config.py
├── requirements.txt
├── README.md
├── mechanic_shop_api_collection.json

---

## ⚙️ Setup Instructions

### 1️⃣ Clone repo

```bash
git clone <your-repo-url>
cd mechanic_shop_api
2️⃣ Create virtual environment
python -m venv venv
.\venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Configure database

Update config.py:

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:password@localhost/mechanic_shop_db"
5️⃣ Initialize database
python -m flask shell
from app import create_app
from app.extensions import db

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()
6️⃣ Run the server
flask run
🔑 Authentication

All protected routes require:

Authorization: Bearer <token>
📬 API Endpoints
👤 Customers
POST /customers/
POST /customers/login
GET /customers/ (Admin, paginated)
GET /customers/my-tickets
PUT /customers/<id>
DELETE /customers/<id>
🛠️ Mechanics
POST /mechanics/ (Admin)
POST /mechanics/login
GET /mechanics/
GET /mechanics/<id>
PUT /mechanics/<id>
DELETE /mechanics/<id> (Admin)
GET /mechanics/most-active
GET /mechanics/my-tickets
🎟️ Service Tickets
POST /service-tickets/
GET /service-tickets/
PUT /assign-mechanic
PUT /remove-mechanic
PUT /edit ⭐ (Advanced Query)
PUT /complete
PUT /add-part
📦 Inventory
POST /inventory/ (Admin)
GET /inventory/
GET /inventory/<id>
PUT /inventory/<id> (Admin)
DELETE /inventory/<id> (Admin)
🧠 Advanced Query Example
PUT /service-tickets/<ticket_id>/edit
{
  "add_ids": [1, 2],
  "remove_ids": [3]
}
🧪 Testing

A Postman collection is included:

mechanic_shop_api_collection.json

Import into Postman to test all routes.

🔄 Example Workflow
Create customer
Create admin
Login → get tokens
Create mechanic
Create service ticket
Add inventory part
Assign mechanic
Add part to ticket
Run advanced query
❗ Notes
Tokens may expire — re-login if needed
Admin-only routes require admin token

Pagination:

/customers?page=1&per_page=5
👨‍💻 Author

Jytre Berry

🏁 Status

✔ Completed
✔ Fully tested
✔ Includes optional challenges
✔ Production-style API design
```
