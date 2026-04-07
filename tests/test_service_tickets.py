import unittest

from app import create_app
from app.extensions import db
from app.models import Customer, Mechanic, Inventory, ServiceTicket


class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.customer = Customer(
                name="Test Customer",
                email="customer@test.com",
                phone="1234567890",
                is_admin=False
            )
            self.customer.set_password("password123")

            self.admin = Customer(
                name="Admin User",
                email="admin@test.com",
                phone="9999999999",
                is_admin=True
            )
            self.admin.set_password("adminpass123")

            self.mechanic = Mechanic(
                name="Test Mechanic",
                email="mech@test.com",
                phone="4445556666",
                salary=55000
            )
            self.mechanic.set_password("password123")

            self.part = Inventory(
                name="Brake Pad",
                price=50.00
            )

            db.session.add_all([self.customer, self.admin, self.mechanic, self.part])
            db.session.commit()

            self.ticket = ServiceTicket(
                vin="1HGCM82633A123456",
                service_date="2026-01-01",
                service_desc="Brake inspection",
                customer_id=self.customer.id
            )
            db.session.add(self.ticket)
            db.session.commit()

            self.ticket_id = self.ticket.id
            self.mechanic_id = self.mechanic.id
            self.part_id = self.part.id

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def login_customer(self):
        response = self.client.post("/customers/login", json={
            "email": "customer@test.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        return response.get_json()["token"]

    def login_admin(self):
        response = self.client.post("/customers/login", json={
            "email": "admin@test.com",
            "password": "adminpass123"
        })
        self.assertEqual(response.status_code, 200)
        return response.get_json()["token"]

    def login_mechanic(self):
        response = self.client.post("/mechanics/login", json={
            "email": "mech@test.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        return response.get_json()["token"]

    def test_create_ticket(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "vin": "1HGCM82633A123456",
            "service_date": "2026-01-01",
            "service_desc": "Oil change"
        }

        response = self.client.post("/service-tickets/", json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_create_ticket_invalid(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "vin": "short",
            "service_date": "2026-01-01"
        }

        response = self.client.post("/service-tickets/", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_get_tickets(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/service-tickets/", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_tickets_forbidden_for_customer(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/service-tickets/", headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_assign_mechanic_to_ticket(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}",
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

    def test_assign_mechanic_not_found(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/assign-mechanic/9999",
            headers=headers
        )

        self.assertEqual(response.status_code, 404)

    def test_assign_mechanic_to_ticket_unauthorized(self):
        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}"
        )

        self.assertEqual(response.status_code, 401)

    def test_remove_mechanic_from_ticket(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        self.client.put(
            f"/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}",
            headers=headers
        )

        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}",
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

    def test_edit_ticket_mechanics(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "add_ids": [self.mechanic_id],
            "remove_ids": []
        }

        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/edit",
            json=payload,
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

    def test_add_part_to_ticket(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/add-part/{self.part_id}",
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

    def test_add_part_not_found(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/add-part/9999",
            headers=headers
        )

        self.assertEqual(response.status_code, 404)

    def test_complete_ticket(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/complete",
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

    def test_complete_ticket_not_found(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.put("/service-tickets/9999/complete", headers=headers)
        self.assertEqual(response.status_code, 404)