from flask import request, g

from ...auth import roles_required
from ...extensions import db, cache
from ...models import ServiceTicket, Mechanic, Inventory
from . import service_tickets_bp
from .schemas import ServiceTicketSchema

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)


@service_tickets_bp.post("/")
@roles_required("customer", "admin")
def create_ticket():
    payload = request.get_json(silent=True) or {}

    try:
        if g.current_role == "admin" and "customer_id" in payload:
            payload["customer_id"] = payload["customer_id"]
        else:
            payload["customer_id"] = g.current_user_id

        ticket = ticket_schema.load(payload)
        db.session.add(ticket)
        db.session.commit()

        cache.clear()

        return ticket_schema.jsonify(ticket), 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


@service_tickets_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
@roles_required("admin", "mechanic")
def assign_mechanic(ticket_id: int, mechanic_id: int):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
        cache.clear()

    return ticket_schema.jsonify(ticket), 200


@service_tickets_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
@roles_required("admin", "mechanic")
def remove_mechanic(ticket_id: int, mechanic_id: int):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
        cache.clear()

    return ticket_schema.jsonify(ticket), 200


@service_tickets_bp.put("/<int:ticket_id>/edit")
@roles_required("admin", "mechanic")
def edit_ticket_mechanics(ticket_id: int):
    ticket = ServiceTicket.query.get_or_404(ticket_id)

    payload = request.get_json(silent=True) or {}
    add_ids = payload.get("add_ids", [])
    remove_ids = payload.get("remove_ids", [])

    if not isinstance(add_ids, list) or not isinstance(remove_ids, list):
        return {"error": "add_ids and remove_ids must both be lists."}, 400

    added = []
    removed = []

    for mechanic_id in remove_ids:
        mechanic = Mechanic.query.get(mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
            removed.append(mechanic.id)

    for mechanic_id in add_ids:
        mechanic = Mechanic.query.get(mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
            added.append(mechanic.id)

    db.session.commit()
    cache.clear()

    return {
        "message": f"Service ticket {ticket_id} updated successfully.",
        "added_ids": added,
        "removed_ids": removed,
        "ticket": ticket_schema.dump(ticket)
    }, 200


@service_tickets_bp.put("/<int:ticket_id>/add-part/<int:part_id>")
@roles_required("admin", "mechanic")
def add_part_to_ticket(ticket_id: int, part_id: int):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    part = Inventory.query.get_or_404(part_id)

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()
        cache.clear()

    return {
        "message": f"Part {part_id} added to service ticket {ticket_id}.",
        "ticket": ticket_schema.dump(ticket)
    }, 200


@service_tickets_bp.get("/")
@roles_required("admin", "mechanic")
@cache.cached(timeout=60)
def get_tickets():
    tickets = ServiceTicket.query.order_by(ServiceTicket.id.asc()).all()
    return tickets_schema.jsonify(tickets), 200


@service_tickets_bp.put("/<int:id>/complete")
@roles_required("admin", "mechanic")
def complete_ticket(id: int):
    ticket = ServiceTicket.query.get_or_404(id)

    cache.clear()

    return {
        "message": f"Service ticket {id} marked as completed."
    }, 200