from flask import request
from marshmallow import ValidationError

from ...auth import roles_required, admin_required
from ...extensions import db, cache
from ...models import Inventory
from . import inventory_bp
from .schemas import InventorySchema

inventory_schema = InventorySchema()
inventory_list_schema = InventorySchema(many=True)


@inventory_bp.post("/")
@admin_required
def create_part():
    payload = request.get_json(silent=True) or {}

    try:
        part = inventory_schema.load(payload)
        db.session.add(part)
        db.session.commit()
        cache.clear()
        return inventory_schema.jsonify(part), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


@inventory_bp.get("/")
@roles_required("admin", "mechanic")
@cache.cached(timeout=60)
def get_parts():
    parts = Inventory.query.order_by(Inventory.id.asc()).all()
    return inventory_list_schema.jsonify(parts), 200


@inventory_bp.get("/<int:id>")
@roles_required("admin", "mechanic")
def get_part(id: int):
    part = Inventory.query.get_or_404(id)
    return inventory_schema.jsonify(part), 200


@inventory_bp.put("/<int:id>")
@admin_required
def update_part(id: int):
    part = Inventory.query.get_or_404(id)
    payload = request.get_json(silent=True) or {}

    if "name" in payload:
        part.name = payload["name"]
    if "price" in payload:
        part.price = payload["price"]

    try:
        db.session.commit()
        cache.clear()
        return inventory_schema.jsonify(part), 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


@inventory_bp.delete("/<int:id>")
@admin_required
def delete_part(id: int):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    cache.clear()
    return {"message": f"Inventory part {id} deleted."}, 200