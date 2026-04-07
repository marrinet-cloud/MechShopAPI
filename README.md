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

## ⚙️ Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Flask-Limiter
- Flask-Caching
- Flask-Swagger & Flask-Swagger-UI
- JWT Authentication
- SQLite (Testing)
- MySQL (Development)
- unittest

---

## 🧩 Project Structure

mechanic_shop_api/
│
├── app/
│ ├── blueprints/
│ │ ├── customers/
│ │ ├── mechanics/
│ │ ├── service_tickets/
│ │ └── inventory/
│ ├── models/
│ ├── schemas/
│ ├── static/
│ │ └── swagger.yaml
│ ├── auth.py
│ ├── extensions.py
│ └── init.py
│
├── tests/
│ ├── test_customers.py
│ ├── test_mechanics.py
│ ├── test_inventory.py
│ └── test_service_tickets.py
│
├── config.py
├── app.py
└── README.md

---

## 🔐 Authentication & Authorization

This API uses **JWT authentication**.

After login, a token is returned and must be included in requests:

Authorization: Bearer <your_token>

### Roles:

- **Customer** → Access personal data and tickets
- **Mechanic** → View assigned service tickets
- **Admin** → Full access to all resources

---

## 📘 API Documentation (Swagger)

Swagger UI is available at:

http://127.0.0.1:5000/api/docs

Each route includes:

- Endpoint path
- HTTP method
- Request parameters
- Authentication requirements
- Example responses

---

## 🔧 Features

### Customers

- Create account
- Login
- View personal tickets
- Update/delete account

### Mechanics

- Create (admin only)
- Login
- View assigned tickets
- Update profile

### Service Tickets

- Create tickets
- Assign/remove mechanics
- Add parts from inventory
- Mark tickets as complete

### Inventory

- Add parts (admin only)
- View inventory
- Update/delete parts

---

## 🧪 Testing

This project includes a full test suite using Python’s unittest framework.

### Run tests:

````bash
python -m unittest discover tests
Tests include:

CRUD operations
Authentication checks
Authorization checks
Negative test cases (invalid input, forbidden access, not found)
🚀 Running the Application
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd mechanic_shop_api
2. Create virtual environment
python -m venv venv
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Run the app
python app.py
🗄️ Configuration
Development → MySQL database
Testing → SQLite database

Set config inside config.py.

📈 Future Improvements
Replace deprecated SQLAlchemy .query.get() with db.session.get()
Improve token expiration handling
Add pagination to more endpoints
Add frontend client
👤 Author

Jytre Berry

✅ Summary

This project demonstrates a fully functional, documented, and tested REST API with authentication, authorization, and relational data handling using Flask.


---

# 🔥 What makes this README strong

- Clean structure
- Covers all rubric requirements
- Shows professionalism
- Mentions Swagger + Testing (big grading points)
- Easy for instructor to run

---

# ⚡ OPTIONAL (extra polish)

After pushing, edit this line:

```md
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
````
