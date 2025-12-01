"""Flask web application for managing warehouse instances."""

from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto


app = Flask(__name__)

# In-memory storage for warehouse instances
warehouses = {}


def get_warehouse(warehouse_id):
    """Get a warehouse by ID, return None if not found."""
    return warehouses.get(warehouse_id)


def parse_warehouse_form():
    """Parse and validate warehouse creation form data."""
    name = request.form.get("name", "").strip()
    capacity = request.form.get("capacity", "0")
    initial = request.form.get("initial_saldo", "0")

    try:
        return name, float(capacity), float(initial), None
    except ValueError:
        return None, 0, 0, "Invalid number format"


def save_new_warehouse(name, capacity, initial):
    """Save a new warehouse and return its ID."""
    warehouse_id = len(warehouses) + 1
    warehouses[warehouse_id] = {
        "name": name,
        "varasto": Varasto(capacity, initial)
    }
    return warehouse_id


@app.route("/")
def index():
    """Display list of all warehouses."""
    return render_template("index.html", warehouses=warehouses)


@app.route("/create", methods=["GET", "POST"])
def create_warehouse():
    """Create a new warehouse."""
    if request.method == "POST":
        name, capacity, initial, error = parse_warehouse_form()
        if error:
            return render_template("create.html", error=error)
        if not name:
            return render_template("create.html", error="Name is required")
        save_new_warehouse(name, capacity, initial)
        return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/warehouse/<int:warehouse_id>")
def view_warehouse(warehouse_id):
    """View details of a specific warehouse."""
    warehouse = get_warehouse(warehouse_id)
    if warehouse is None:
        return redirect(url_for("index"))

    return render_template(
        "warehouse.html",
        warehouse_id=warehouse_id,
        warehouse=warehouse
    )


@app.route("/warehouse/<int:warehouse_id>/add", methods=["POST"])
def add_items(warehouse_id):
    """Add items to a warehouse."""
    warehouse = get_warehouse(warehouse_id)
    if warehouse is None:
        return redirect(url_for("index"))

    amount = request.form.get("amount", "0")
    try:
        amount = float(amount)
    except ValueError:
        amount = 0

    warehouse["varasto"].lisaa_varastoon(amount)
    return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))


@app.route("/warehouse/<int:warehouse_id>/remove", methods=["POST"])
def remove_items(warehouse_id):
    """Remove items from a warehouse."""
    warehouse = get_warehouse(warehouse_id)
    if warehouse is None:
        return redirect(url_for("index"))

    amount = request.form.get("amount", "0")
    try:
        amount = float(amount)
    except ValueError:
        amount = 0

    warehouse["varasto"].ota_varastosta(amount)
    return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))


if __name__ == "__main__":
    app.run(debug=True)
