from marshmallow import fields, validate

from ...extensions import ma
from ...models import Mechanic


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=6)
    )

    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True