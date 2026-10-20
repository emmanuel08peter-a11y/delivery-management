from database import get_connection


# ==========================================
# CUSTOMER CLASS
# ==========================================

class Customer:

    def __init__(self, name, phone, address):

        self.customer_id = None
        self.name = name
        self.phone = phone
        self.address = address

    def save(self):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO customers (name, phone, address)
                VALUES (?, ?, ?)
            """, (self.name, self.phone, self.address))

            self.customer_id = cursor.lastrowid

            connection.commit()

            print("Customer registered successfully!")

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()


# ==========================================
# RIDER CLASS
# ==========================================

class Rider:

    def __init__(self, name, phone):

        self.rider_id = None
        self.name = name
        self.phone = phone

    def save(self):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO riders (name, phone)
                VALUES (?, ?)
            """, (self.name, self.phone))

            self.rider_id = cursor.lastrowid

            connection.commit()

            print("Delivery rider registered successfully!")

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()


# ==========================================
# ORDER CLASS
# ==========================================

class Order:

    ALLOWED_STATUSES = [
        "Pending",
        "Assigned",
        "Out for Delivery",
        "Delivered",
        "Cancelled"
    ]

    def __init__(
        self,
        customer_id,
        pickup_address,
        delivery_address,
        description,
        order_amount,
        delivery_fee
    ):

        self.order_id = None
        self.customer_id = customer_id
        self.rider_id = None

        self.pickup_address = pickup_address
        self.delivery_address = delivery_address
        self.description = description

        self.order_amount = order_amount
        self.delivery_fee = delivery_fee

        self.status = "Pending"

    def save(self):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO orders (
                    customer_id,
                    pickup_address,
                    delivery_address,
                    description,
                    order_amount,
                    delivery_fee,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.customer_id,
                self.pickup_address,
                self.delivery_address,
                self.description,
                self.order_amount,
                self.delivery_fee,
                self.status
            ))

            self.order_id = cursor.lastrowid

            connection.commit()

            print("Delivery order created successfully!")

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def assign_rider(self, rider_id):

        if self.order_id is None:
            raise ValueError("Save the order before assigning a rider.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT status
                FROM orders
                WHERE order_id = ?
            """, (self.order_id,))

            record = cursor.fetchone()

            if record is None:
                raise ValueError("Order not found.")

            if record[0] in ("Delivered", "Cancelled"):
                raise ValueError(
                    "Completed or cancelled orders cannot be assigned."
                )

            cursor.execute("""
                SELECT rider_id
                FROM riders
                WHERE rider_id = ?
            """, (rider_id,))

            if cursor.fetchone() is None:
                raise ValueError("The selected rider does not exist.")

            cursor.execute("""
                UPDATE orders
                SET rider_id = ?, status = 'Assigned'
                WHERE order_id = ?
            """, (rider_id, self.order_id))

            connection.commit()

            self.rider_id = rider_id
            self.status = "Assigned"

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def update_status(self, new_status):

        if self.order_id is None:
            raise ValueError("Save the order before updating its status.")

        if new_status not in self.ALLOWED_STATUSES:
            raise ValueError("Invalid order status.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT status, rider_id
                FROM orders
                WHERE order_id = ?
            """, (self.order_id,))

            record = cursor.fetchone()

            if record is None:
                raise ValueError("Order not found.")

            current_status, rider_id = record

            if current_status in ("Delivered", "Cancelled"):
                raise ValueError(
                    "Completed or cancelled orders cannot be changed."
                )

            if (
                new_status in ("Assigned", "Out for Delivery")
                and rider_id is None
            ):
                raise ValueError(
                    "Assign a rider before using this status."
                )

            cursor.execute("""
                UPDATE orders
                SET status = ?
                WHERE order_id = ?
            """, (new_status, self.order_id))

            connection.commit()

            self.status = new_status

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()