from flask import request, g
from marshmallow import ValidationError, Schema, fields
from sqlalchemy.exc import IntegrityError

from ...auth import encode_token, roles_required, admin_required
from ...extensions import db, limiter, cache
from ...models import Customer, ServiceTicket
from . import customers_bp
from .schemas import CustomerSchema


class CustomerLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = CustomerLoginSchema()


@customers_bp.post("/")
@limiter.limit("5 per minute")
def create_customer():
    payload = request.get_json(silent=True) or {}

    try:
        customer = customer_schema.load(payload)
        customer.set_password(customer.password)
        
        db.session.add(customer)
        db.session.commit()

        cache.clear()

        return customer_schema.jsonify(customer), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email must be unique. A customer with that email already exists."}, 409
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


@customers_bp.post("/login")
@limiter.limit("10 per minute")
def login_customer():
    payload = request.get_json(silent=True) or {}

    try:
        credentials = login_schema.load(payload)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    customer = Customer.query.filter_by(email=credentials["email"]).first()

    if not customer or not customer.check_password(credentials["password"]):
        return {"error": "Invalid email or password."}, 401

    token = encode_token(customer.id, customer.is_admin)

    return {
        "message": "Login successful.",
        "token": token,
        "customer_id": customer.id,
        "role": "admin" if customer.is_admin else "customer"
    }, 200


@customers_bp.get("/")
@admin_required
@cache.cached(timeout=60, query_string=True)
def get_customers():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if page < 1:
        return {"error": "page must be 1 or greater."}, 400

    if per_page < 1 or per_page > 100:
        return {"error": "per_page must be between 1 and 100."}, 400

    pagination = Customer.query.order_by(Customer.id.asc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "customers": customers_schema.dump(pagination.items)
    }, 200


@customers_bp.get("/my-tickets")
@roles_required("customer", "admin")
def get_my_tickets():
    customer_id = g.current_user_id

    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).order_by(ServiceTicket.id.asc()).all()

    return {
        "customer_id": customer_id,
        "service_tickets": [
            {
                "id": ticket.id,
                "vin": ticket.vin,
                "service_date": ticket.service_date,
                "service_desc": ticket.service_desc,
                "customer_id": ticket.customer_id
            }
            for ticket in tickets
        ]
    }, 200


@customers_bp.put("/<int:id>")
@roles_required("customer", "admin")
def update_customer(id: int):
    if g.current_role == "customer" and g.current_user_id != id:
        return {"error": "You are not authorized to update this customer."}, 403

    customer = Customer.query.get_or_404(id)
    payload = request.get_json(silent=True) or {}

    if "name" in payload:
        customer.name = payload["name"]
    if "email" in payload:
        customer.email = payload["email"]
    if "phone" in payload:
        customer.phone = payload["phone"]
    if "password" in payload:
        customer.set_password(payload["password"])

    if g.current_role == "admin" and "is_admin" in payload:
        customer.is_admin = bool(payload["is_admin"])

    try:
        db.session.commit()
        cache.clear()
        return customer_schema.jsonify(customer), 200
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email must be unique. A customer with that email already exists."}, 409
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


@customers_bp.delete("/<int:id>")
@roles_required("customer", "admin")
def delete_customer(id: int):
    if g.current_role == "customer" and g.current_user_id != id:
        return {"error": "You are not authorized to delete this customer."}, 403

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()

    cache.clear()

    return {"message": f"Customer {id} deleted."}, 200