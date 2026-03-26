from flask import request
from sqlalchemy.exc import IntegrityError

from ...extensions import db
from ...models import Customer
from . import customers_bp
from .schemas import CustomerSchema

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


@customers_bp.post("/")
def create_customer():
    payload = request.get_json(silent=True) or {}
    try:
        customer = customer_schema.load(payload)
        db.session.add(customer)
        db.session.commit()
        return customer_schema.jsonify(customer), 201
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email must be unique. A customer with that email already exists."}, 409
    except Exception as e:
        return {"error": str(e)}, 400


@customers_bp.get("/")
def get_customers():
    customers = Customer.query.order_by(Customer.id.asc()).all()
    return customers_schema.jsonify(customers), 200


@customers_bp.put("/<int:id>")
def update_customer(id: int):
    customer = Customer.query.get_or_404(id)
    payload = request.get_json(silent=True) or {}

    if "name" in payload:
        customer.name = payload["name"]
    if "email" in payload:
        customer.email = payload["email"]
    if "phone" in payload:
        customer.phone = payload["phone"]

    try:
        db.session.commit()
        return customer_schema.jsonify(customer), 200
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email must be unique. A customer with that email already exists."}, 409


@customers_bp.delete("/<int:id>")
def delete_customer(id: int):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return {"message": f"Customer {id} deleted."}, 200
