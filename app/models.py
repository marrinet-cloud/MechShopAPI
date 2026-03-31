from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


inventory_service_tickets = db.Table(
    "inventory_service_tickets",
    db.Column("ticket_id", db.Integer, db.ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("inventory_id", db.Integer, db.ForeignKey("inventory.id"), primary_key=True)
)


class ServiceMechanic(db.Model):
    __tablename__ = "service_mechanics"

    ticket_id = db.Column(db.Integer, ForeignKey("service_tickets.id"), primary_key=True)
    mechanic_id = db.Column(db.Integer, ForeignKey("mechanics.id"), primary_key=True)


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    service_tickets = relationship(
        "ServiceTicket",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    def set_password(self, raw_password: str) -> None:
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password, raw_password)


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    service_tickets = relationship(
        "ServiceTicket",
        secondary="service_mechanics",
        back_populates="mechanics"
    )

    def set_password(self, raw_password: str) -> None:
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password, raw_password)


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    service_tickets = relationship(
        "ServiceTicket",
        secondary=inventory_service_tickets,
        back_populates="parts"
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vin = db.Column(db.String(17), nullable=False)
    service_date = db.Column(db.String(50), nullable=False)
    service_desc = db.Column(db.String(500), nullable=False)
    customer_id = db.Column(db.Integer, ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="service_tickets")

    mechanics = relationship(
        "Mechanic",
        secondary="service_mechanics",
        back_populates="service_tickets"
    )

    parts = relationship(
        "Inventory",
        secondary=inventory_service_tickets,
        back_populates="service_tickets"
    )