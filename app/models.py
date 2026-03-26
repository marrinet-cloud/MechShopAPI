from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .extensions import db


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

    service_tickets = relationship(
        "ServiceTicket",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    service_tickets = relationship(
        "ServiceTicket",
        secondary="service_mechanics",
        back_populates="mechanics"
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
