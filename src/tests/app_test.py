"""Unit tests for the Flask warehouse web application."""

import unittest
from app import app, warehouses


class TestFlaskApp(unittest.TestCase):
    """Test suite for Flask web application endpoints."""

    def setUp(self):
        """Set up test client and reset warehouses."""
        self.client = app.test_client()
        app.config["TESTING"] = True
        warehouses.clear()

    def test_index_empty(self):
        """Index page shows no warehouses message when empty."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No warehouses yet", response.data)

    def test_index_with_warehouses(self):
        """Index page lists existing warehouses."""
        self.client.post("/create", data={
            "name": "Test Warehouse",
            "capacity": "100",
            "initial_saldo": "0"
        })
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Warehouse", response.data)

    def test_create_page_get(self):
        """Create page renders correctly on GET."""
        response = self.client.get("/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create New Warehouse", response.data)

    def test_create_warehouse_success(self):
        """Creating a warehouse redirects to index."""
        response = self.client.post("/create", data={
            "name": "New Warehouse",
            "capacity": "50",
            "initial_saldo": "10"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"New Warehouse", response.data)

    def test_create_warehouse_invalid_number(self):
        """Invalid number format shows error."""
        response = self.client.post("/create", data={
            "name": "Bad Warehouse",
            "capacity": "not_a_number",
            "initial_saldo": "0"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid number format", response.data)

    def test_create_warehouse_empty_name(self):
        """Empty name shows error."""
        response = self.client.post("/create", data={
            "name": "",
            "capacity": "100",
            "initial_saldo": "0"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Name is required", response.data)

    def test_view_warehouse(self):
        """View warehouse page shows warehouse details."""
        self.client.post("/create", data={
            "name": "Detail Warehouse",
            "capacity": "100",
            "initial_saldo": "25"
        })
        response = self.client.get("/warehouse/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail Warehouse", response.data)

    def test_view_nonexistent_warehouse(self):
        """Viewing nonexistent warehouse redirects to index."""
        response = self.client.get(
            "/warehouse/999",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_add_items_to_warehouse(self):
        """Adding items increases warehouse stock."""
        self.client.post("/create", data={
            "name": "Add Test",
            "capacity": "100",
            "initial_saldo": "0"
        })
        self.client.post("/warehouse/1/add", data={"amount": "50"})
        self.assertEqual(warehouses[1]["varasto"].saldo, 50)

    def test_remove_items_from_warehouse(self):
        """Removing items decreases warehouse stock."""
        self.client.post("/create", data={
            "name": "Remove Test",
            "capacity": "100",
            "initial_saldo": "80"
        })
        self.client.post("/warehouse/1/remove", data={"amount": "30"})
        self.assertEqual(warehouses[1]["varasto"].saldo, 50)

    def test_add_items_nonexistent_warehouse(self):
        """Adding to nonexistent warehouse redirects."""
        response = self.client.post(
            "/warehouse/999/add",
            data={"amount": "10"},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_remove_items_nonexistent_warehouse(self):
        """Removing from nonexistent warehouse redirects."""
        response = self.client.post(
            "/warehouse/999/remove",
            data={"amount": "10"},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
