import unittest

from app import create_app
from app.extensions import db
from app.models import Customer, Inventory


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.admin = Customer(
                name="Admin",
                email="admin@test.com",
                phone="1234567890",
                is_admin=True
            )
            self.admin.set_password("password123")

            self.customer = Customer(
                name="Regular User",
                email="user@test.com",
                phone="5551110000",
                is_admin=False
            )
            self.customer.set_password("password123")

            self.part = Inventory(
                name="Starter Motor",
                price=120.00
            )

            db.session.add_all([self.admin, self.customer, self.part])
            db.session.commit()

            self.part_id = self.part.id

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def login_admin(self):
        response = self.client.post("/customers/login", json={
            "email": "admin@test.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        return response.get_json()["token"]

    def login_customer(self):
        response = self.client.post("/customers/login", json={
            "email": "user@test.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        return response.get_json()["token"]

    def test_create_inventory(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "name": "Brake Pad",
            "price": 50.0
        }

        response = self.client.post("/inventory/", json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_get_inventory(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/inventory/", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_inventory_unauthorized(self):
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 401)

    def test_get_inventory_forbidden_for_customer(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/inventory/", headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_get_inventory_part_by_id(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get(f"/inventory/{self.part_id}", headers=headers)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Starter Motor")

    def test_get_inventory_part_not_found(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/inventory/9999", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_update_inventory_part(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "name": "Updated Starter Motor",
            "price": 140.00
        }

        response = self.client.put(
            f"/inventory/{self.part_id}",
            json=payload,
            headers=headers
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Updated Starter Motor")

    def test_delete_inventory_part(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.delete(
            f"/inventory/{self.part_id}",
            headers=headers
        )

        self.assertEqual(response.status_code, 200)