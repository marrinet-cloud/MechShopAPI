from marshmallow import fields
from ...extensions import ma
from ...models import ServiceTicket
from ..mechanics.schemas import MechanicSchema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema(many=True), dump_only=True)

    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True
