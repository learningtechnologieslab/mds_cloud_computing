"""
Flask RESTful API - CRUD Operations
Database: MySQL classicmodels
Tables: orders, orderdetails
Approach: Functional (non-OOP)
"""

from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# ─────────────────────────────────────────────
# Database Configuration
# ─────────────────────────────────────────────
DB_HOST     = "mdsmysql.sci.pitt.edu"
DB_PORT     = 3306
DB_NAME     = "classicmodels"
DB_USER     = "webTestUser"
DB_PASSWORD = "Md3W3bUs@r"


def get_connection():
    """Create and return a new MySQL connection."""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# ═══════════════════════════════════════════════════════════════
#  ORDERS  –  /api/orders
# ═══════════════════════════════════════════════════════════════

# ── GET all orders ──────────────────────────────────────────────
@app.route("/api/orders", methods=["GET"])
def get_orders():
    """Return all orders."""
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders ORDER BY orderNumber")
        orders = cursor.fetchall()
        # Convert date objects to ISO strings for JSON serialisation
        for o in orders:
            for key in ("orderDate", "requiredDate", "shippedDate"):
                if o.get(key):
                    o[key] = o[key].isoformat()
        return jsonify({"success": True, "data": orders, "count": len(orders)}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ── GET a single order ──────────────────────────────────────────
@app.route("/api/orders/<int:order_number>", methods=["GET"])
def get_order(order_number):
    """Return a single order by orderNumber."""
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE orderNumber = %s", (order_number,))
        order = cursor.fetchone()
        if not order:
            return jsonify({"success": False, "error": "Order not found"}), 404
        for key in ("orderDate", "requiredDate", "shippedDate"):
            if order.get(key):
                order[key] = order[key].isoformat()
        return jsonify({"success": True, "data": order}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ── POST create a new order ─────────────────────────────────────
@app.route("/api/orders", methods=["POST"])
def create_order():
    """
    Create a new order.
    Required JSON body fields:
        orderNumber, orderDate, requiredDate, status, customerNumber
    Optional:
        shippedDate, comments
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "JSON body required"}), 400

    required = ["orderNumber", "orderDate", "requiredDate", "status", "customerNumber"]
    missing  = [f for f in required if f not in data]
    if missing:
        return jsonify({"success": False, "error": f"Missing fields: {missing}"}), 400

    sql = """
        INSERT INTO orders
            (orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data["orderNumber"],
        data["orderDate"],
        data["requiredDate"],
        data.get("shippedDate"),
        data["status"],
        data.get("comments"),
        data["customerNumber"],
    )

    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"success": True, "message": "Order created", "orderNumber": data["orderNumber"]}), 201
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ── PUT update an existing order ────────────────────────────────
@app.route("/api/orders/<int:order_number>", methods=["PUT"])
def update_order(order_number):
    """
    Update an existing order.
    Accepts any subset of: orderDate, requiredDate, shippedDate,
                           status, comments, customerNumber
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "JSON body required"}), 400

    allowed_fields = ["orderDate", "requiredDate", "shippedDate", "status", "comments", "customerNumber"]
    updates = {k: v for k, v in data.items() if k in allowed_fields}
    if not updates:
        return jsonify({"success": False, "error": "No valid fields provided for update"}), 400

    set_clause = ", ".join(f"{col} = %s" for col in updates)
    sql        = f"UPDATE orders SET {set_clause} WHERE orderNumber = %s"
    values     = list(updates.values()) + [order_number]

    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Order not found"}), 404
        return jsonify({"success": True, "message": "Order updated"}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ── DELETE an order ─────────────────────────────────────────────
@app.route("/api/orders/<int:order_number>", methods=["DELETE"])
def delete_order(order_number):
    """
    Delete an order and its associated orderdetails (cascade).
    orderdetails rows are deleted first to respect the FK constraint.
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        # Delete child records first
        cursor.execute("DELETE FROM orderdetails WHERE orderNumber = %s", (order_number,))
        cursor.execute("DELETE FROM orders WHERE orderNumber = %s", (order_number,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Order not found"}), 404
        return jsonify({"success": True, "message": "Order and its details deleted"}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ═══════════════════════════════════════════════════════════════
#  ORDER DETAILS  –  /api/orders/<orderNumber>/details
# ═══════════════════════════════════════════════════════════════

# ── GET all details for an order ────────────────────────────────
@app.route("/api/orders/<int:order_number>/details", methods=["GET"])
def get_order_details(order_number):
    """Return all line items for a given order."""
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM orderdetails WHERE orderNumber = %s ORDER BY orderLineNumber",
            (order_number,)
        )
        details = cursor.fetchall()
        if not details:
            return jsonify({"success": False, "error": "No details found for this order"}), 404
        return jsonify({"success": True, "data": details, "count": len(details)}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ── GET a single order detail line ──────────────────────────────
@app.route("/api/orders/<int:order_number>/details/<int:line_number>", methods=["GET"])
def get_order_detail(order_number, line_number):
    """Return a specific line item."""
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM orderdetails WHERE orderNumber = %s AND orderLineNumber = %s",
            (order_number, line_number)
        )
        detail = cursor.fetchone()
        if not detail:
            return jsonify({"success": False, "error": "Order detail not found"}), 404
        return jsonify({"success": True, "data": detail}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ── POST add a detail line to an order ─────────────────────────
@app.route("/api/orders/<int:order_number>/details", methods=["POST"])
def create_order_detail(order_number):
    """
    Add a new line item to an order.
    Required JSON body fields:
        orderLineNumber, productCode, quantityOrdered, priceEach
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "JSON body required"}), 400

    required = ["orderLineNumber", "productCode", "quantityOrdered", "priceEach"]
    missing  = [f for f in required if f not in data]
    if missing:
        return jsonify({"success": False, "error": f"Missing fields: {missing}"}), 400

    sql = """
        INSERT INTO orderdetails
            (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
        VALUES
            (%s, %s, %s, %s, %s)
    """
    values = (
        order_number,
        data["productCode"],
        data["quantityOrdered"],
        data["priceEach"],
        data["orderLineNumber"],
    )

    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"success": True, "message": "Order detail created"}), 201
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ── PUT update a detail line ────────────────────────────────────
@app.route("/api/orders/<int:order_number>/details/<int:line_number>", methods=["PUT"])
def update_order_detail(order_number, line_number):
    """
    Update a line item.
    Accepts any subset of: productCode, quantityOrdered, priceEach
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "JSON body required"}), 400

    allowed_fields = ["productCode", "quantityOrdered", "priceEach"]
    updates = {k: v for k, v in data.items() if k in allowed_fields}
    if not updates:
        return jsonify({"success": False, "error": "No valid fields provided for update"}), 400

    set_clause = ", ".join(f"{col} = %s" for col in updates)
    sql        = f"UPDATE orderdetails SET {set_clause} WHERE orderNumber = %s AND orderLineNumber = %s"
    values     = list(updates.values()) + [order_number, line_number]

    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Order detail not found"}), 404
        return jsonify({"success": True, "message": "Order detail updated"}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ── DELETE a detail line ─────────────────────────────────────────
@app.route("/api/orders/<int:order_number>/details/<int:line_number>", methods=["DELETE"])
def delete_order_detail(order_number, line_number):
    """Delete a single line item from an order."""
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM orderdetails WHERE orderNumber = %s AND orderLineNumber = %s",
            (order_number, line_number)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Order detail not found"}), 404
        return jsonify({"success": True, "message": "Order detail deleted"}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
