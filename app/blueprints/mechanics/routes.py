from flask import request
from sqlalchemy.exc import IntegrityError

from ...extensions import db
from ...models import Mechanic
from . import mechanics_bp
from .schemas import MechanicSchema

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


@mechanics_bp.post("/")
def create_mechanic():
    payload = request.get_json(silent=True) or {}
    try:
        mechanic = mechanic_schema.load(payload)
        db.session.add(mechanic)
        db.session.commit()
        return mechanic_schema.jsonify(mechanic), 201
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email must be unique. A mechanic with that email already exists."}, 409
    except Exception as e:
        return {"error": str(e)}, 400


@mechanics_bp.get("/")
def get_mechanics():
    mechanics = Mechanic.query.order_by(Mechanic.id.asc()).all()
    return mechanics_schema.jsonify(mechanics), 200

@mechanics_bp.get("/<int:id>")
def get_mechanic(id: int):
    mechanic = Mechanic.query.get_or_404(id)
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.put("/<int:id>")
def update_mechanic(id: int):
    mechanic = Mechanic.query.get_or_404(id)
    payload = request.get_json(silent=True) or {}

    if "name" in payload:
        mechanic.name = payload["name"]
    if "email" in payload:
        mechanic.email = payload["email"]
    if "phone" in payload:
        mechanic.phone = payload["phone"]
    if "salary" in payload:
        mechanic.salary = payload["salary"]

    try:
        db.session.commit()
        return mechanic_schema.jsonify(mechanic), 200
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email must be unique. A mechanic with that email already exists."}, 409
    except Exception as e:
        return {"error": str(e)}, 400


@mechanics_bp.delete("/<int:id>")
def delete_mechanic(id: int):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return {"message": f"Mechanic {id} deleted."}, 200
