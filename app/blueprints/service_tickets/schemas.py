from marshmallow import fields

from ...extensions import ma
from ...models import ServiceTicket
from ..mechanics.schemas import MechanicSchema
from ..inventory.schemas import InventorySchema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema(many=True), dump_only=True)
    parts = fields.Nested(InventorySchema(many=True), dump_only=True)

    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True