import unittest

from app import create_app
from app.extensions import db
from app.models import Customer


class TestCustomers(unittest.TestCase):
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

            self.other_customer = Customer(
                name="Other Customer",
                email="other@test.com",
                phone="8887776666",
                is_admin=False
            )
            self.other_customer.set_password("password123")

            db.session.add_all([self.customer, self.admin, self.other_customer])
            db.session.commit()

            self.customer_id = self.customer.id
            self.admin_id = self.admin.id
            self.other_customer_id = self.other_customer.id

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

    def test_create_customer(self):
        payload = {
            "name": "Jane Doe",
            "email": "jane@test.com",
            "phone": "5551234567",
            "password": "password123",
            "is_admin": False
        }

        response = self.client.post("/customers/", json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "Jane Doe")
        self.assertEqual(data["email"], "jane@test.com")

    def test_create_customer_invalid(self):
        payload = {
            "name": "Bad User",
            "phone": "5551234567",
            "password": "password123"
        }

        response = self.client.post("/customers/", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_customer_duplicate_email(self):
        payload = {
            "name": "Duplicate",
            "email": "customer@test.com",
            "phone": "5555555555",
            "password": "password123",
            "is_admin": False
        }

        response = self.client.post("/customers/", json=payload)
        self.assertIn(response.status_code, [400, 409])

    def test_login_customer(self):
        response = self.client.post("/customers/login", json={
            "email": "customer@test.com",
            "password": "password123"
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", data)

    def test_login_customer_invalid(self):
        response = self.client.post("/customers/login", json={
            "email": "customer@test.com",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)

    def test_get_customers_as_admin(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/customers/", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_customers_without_token(self):
        response = self.client.get("/customers/")
        self.assertEqual(response.status_code, 401)

    def test_get_customers_forbidden_for_regular_customer(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/customers/", headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_get_my_tickets_customer(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/customers/my-tickets", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_customer_self(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "name": "Updated Customer",
            "phone": "2223334444"
        }

        response = self.client.put(
            f"/customers/{self.customer_id}",
            json=payload,
            headers=headers
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Updated Customer")

    def test_update_customer_unauthorized(self):
        response = self.client.put(
            f"/customers/{self.customer_id}",
            json={"name": "No Auth"}
        )

        self.assertEqual(response.status_code, 401)

    def test_update_other_customer_forbidden(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.put(
            f"/customers/{self.other_customer_id}",
            json={"name": "Hacker"},
            headers=headers
        )

        self.assertEqual(response.status_code, 403)

    def test_update_customer_not_found(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.put(
            "/customers/9999",
            json={"name": "Ghost"},
            headers=headers
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_customer_self(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.delete(
            f"/customers/{self.customer_id}",
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_other_customer_forbidden(self):
        token = self.login_customer()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.delete(
            f"/customers/{self.other_customer_id}",
            headers=headers
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_customer_not_found(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.delete("/customers/9999", headers=headers)
        self.assertEqual(response.status_code, 404)