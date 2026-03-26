from flask import request

from ...extensions import db
from ...models import ServiceTicket, Mechanic
from . import service_tickets_bp
from .schemas import ServiceTicketSchema

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)


@service_tickets_bp.post("/")
def create_ticket():
    payload = request.get_json(silent=True) or {}
    try:
        ticket = ticket_schema.load(payload)
        db.session.add(ticket)
        db.session.commit()
        return ticket_schema.jsonify(ticket), 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


@service_tickets_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
def assign_mechanic(ticket_id: int, mechanic_id: int):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()

    return ticket_schema.jsonify(ticket), 200


@service_tickets_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
def remove_mechanic(ticket_id: int, mechanic_id: int):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()

    return ticket_schema.jsonify(ticket), 200


@service_tickets_bp.get("/")
def get_tickets():
    tickets = ServiceTicket.query.order_by(ServiceTicket.id.asc()).all()
    return tickets_schema.jsonify(tickets), 200

@service_tickets_bp.put("/<int:id>/complete")
def complete_ticket(id: int):
    ticket = ServiceTicket.query.get_or_404(id)
    return {
        "message": f"Service ticket {id} marked as completed."
    }, 200