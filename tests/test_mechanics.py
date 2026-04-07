import unittest

from app import create_app
from app.extensions import db
from app.models import Mechanic, Customer


class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.mechanic = Mechanic(
                name="Test Mechanic",
                email="mech@test.com",
                phone="1234567890",
                salary=50000
            )
            self.mechanic.set_password("password123")

            self.admin = Customer(
                name="Admin User",
                email="admin@test.com",
                phone="9999999999",
                is_admin=True
            )
            self.admin.set_password("adminpass123")

            db.session.add_all([self.mechanic, self.admin])
            db.session.commit()

            self.mechanic_id = self.mechanic.id

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def login_mechanic(self):
        response = self.client.post("/mechanics/login", json={
            "email": "mech@test.com",
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

    def test_create_mechanic_as_admin(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "name": "New Mechanic",
            "email": "newmech@test.com",
            "phone": "5551112222",
            "salary": 65000,
            "password": "password123"
        }

        response = self.client.post("/mechanics/", json=payload, headers=headers)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["email"], "newmech@test.com")

    def test_create_mechanic_duplicate_email(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "name": "Dup Mechanic",
            "email": "mech@test.com",
            "phone": "5550001111",
            "salary": 60000,
            "password": "password123"
        }

        response = self.client.post("/mechanics/", json=payload, headers=headers)
        self.assertIn(response.status_code, [400, 409])

    def test_login_mechanic(self):
        response = self.client.post("/mechanics/login", json={
            "email": "mech@test.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.get_json())

    def test_login_invalid(self):
        response = self.client.post("/mechanics/login", json={
            "email": "wrong@test.com",
            "password": "wrong"
        })

        self.assertEqual(response.status_code, 401)

    def test_get_mechanics(self):
        token = self.login_mechanic()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/mechanics/", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_mechanics_unauthorized(self):
        response = self.client.get("/mechanics/")
        self.assertEqual(response.status_code, 401)

    def test_get_most_active_mechanics(self):
        token = self.login_mechanic()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/mechanics/most-active", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_my_tickets_mechanic(self):
        token = self.login_mechanic()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/mechanics/my-tickets", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_mechanic_by_id(self):
        token = self.login_mechanic()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get(f"/mechanics/{self.mechanic_id}", headers=headers)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["email"], "mech@test.com")

    def test_get_mechanic_not_found(self):
        token = self.login_mechanic()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/mechanics/9999", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_update_mechanic_self(self):
        token = self.login_mechanic()
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "name": "Updated Mechanic",
            "phone": "7778889999"
        }

        response = self.client.put(
            f"/mechanics/{self.mechanic_id}",
            json=payload,
            headers=headers
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Updated Mechanic")

    def test_delete_mechanic_as_admin(self):
        token = self.login_admin()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.delete(
            f"/mechanics/{self.mechanic_id}",
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_mechanic_forbidden_for_mechanic(self):
        token = self.login_mechanic()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.delete(
            f"/mechanics/{self.mechanic_id}",
            headers=headers
        )

        self.assertEqual(response.status_code, 403)