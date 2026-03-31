from marshmallow import fields, validate

from ...extensions import ma
from ...models import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=6)
    )
    is_admin = fields.Boolean(load_default=False)

    class Meta:
        model = Customer
        load_instance = True
        include_fk = True