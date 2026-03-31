from flask import request, g
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError, Schema, fields

from ...auth import encode_mechanic_token, roles_required, admin_required
from ...extensions import db, limiter, cache
from ...models import Mechanic, ServiceTicket
from . import mechanics_bp
from .schemas import MechanicSchema

class MechanicLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
mechanic_login_schema = MechanicLoginSchema()


@mechanics_bp.post("/")
@admin_required
@limiter.limit("5 per minute")
def create_mechanic():
    payload = request.get_json(silent=True) or {}

    try:
        mechanic = mechanic_schema.load(payload)
        mechanic.set_password(mechanic.password)

        db.session.add(mechanic)
        db.session.commit()

        cache.clear()

        return mechanic_schema.jsonify(mechanic), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email must be unique. A mechanic with that email already exists."}, 409
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


@mechanics_bp.post("/login")
@limiter.limit("10 per minute")
def login_mechanic():
    payload = request.get_json(silent=True) or {}

    try:
        credentials = mechanic_login_schema.load(payload)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    mechanic = Mechanic.query.filter_by(email=credentials["email"]).first()

    if not mechanic or not mechanic.check_password(credentials["password"]):
        return {"error": "Invalid email or password."}, 401

    token = encode_mechanic_token(mechanic.id)

    return {
        "message": "Mechanic login successful.",
        "token": token,
        "mechanic_id": mechanic.id,
        "role": "mechanic"
    }, 200


@mechanics_bp.get("/")
@roles_required("admin", "mechanic")
@limiter.limit("10 per minute")
@cache.cached(timeout=60)
def get_mechanics():
    mechanics = Mechanic.query.order_by(Mechanic.id.asc()).all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.get("/most-active")
@roles_required("admin", "mechanic")
@cache.cached(timeout=60)
def get_most_active_mechanics():
    mechanics = (
        db.session.query(
            Mechanic,
            func.count(ServiceTicket.id).label("ticket_count")
        )
        .outerjoin(Mechanic.service_tickets)
        .group_by(Mechanic.id)
        .order_by(func.count(ServiceTicket.id).desc(), Mechanic.id.asc())
        .all()
    )

    return {
        "mechanics": [
            {
                "id": mechanic.id,
                "name": mechanic.name,
                "email": mechanic.email,
                "phone": mechanic.phone,
                "salary": mechanic.salary,
                "ticket_count": ticket_count
            }
            for mechanic, ticket_count in mechanics
        ]
    }, 200


@mechanics_bp.get("/my-tickets")
@roles_required("mechanic")
def get_my_assigned_tickets():
    mechanic = Mechanic.query.get_or_404(g.current_user_id)

    return {
        "mechanic_id": mechanic.id,
        "service_tickets": [
            {
                "id": ticket.id,
                "vin": ticket.vin,
                "service_date": ticket.service_date,
                "service_desc": ticket.service_desc,
                "customer_id": ticket.customer_id
            }
            for ticket in mechanic.service_tickets
        ]
    }, 200


@mechanics_bp.get("/<int:id>")
@roles_required("admin", "mechanic")
def get_mechanic(id: int):
    mechanic = Mechanic.query.get_or_404(id)
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.put("/<int:id>")
@roles_required("admin", "mechanic")
def update_mechanic(id: int):
    if g.current_role == "mechanic" and g.current_user_id != id:
        return {"error": "You are not authorized to update this mechanic."}, 403

    mechanic = Mechanic.query.get_or_404(id)
    payload = request.get_json(silent=True) or {}

    if "name" in payload:
        mechanic.name = payload["name"]
    if "email" in payload:
        mechanic.email = payload["email"]
    if "phone" in payload:
        mechanic.phone = payload["phone"]
    if "salary" in payload and g.current_role == "admin":
        mechanic.salary = payload["salary"]
    if "password" in payload:
        mechanic.set_password(payload["password"])

    try:
        db.session.commit()
        cache.clear()
        return mechanic_schema.jsonify(mechanic), 200
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email must be unique. A mechanic with that email already exists."}, 409
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


@mechanics_bp.delete("/<int:id>")
@admin_required
def delete_mechanic(id: int):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()

    cache.clear()

    return {"message": f"Mechanic {id} deleted."}, 200