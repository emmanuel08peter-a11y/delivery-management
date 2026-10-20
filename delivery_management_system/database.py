import sqlite3
import os


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_NAME = os.path.join(DATA_DIR, "delivery.db")


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

def create_tables():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL
            )
        """)

        # Riders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS riders (
                rider_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)

        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,

                customer_id INTEGER NOT NULL,
                rider_id INTEGER,

                pickup_address TEXT NOT NULL,
                delivery_address TEXT NOT NULL,
                description TEXT NOT NULL,

                order_amount REAL NOT NULL CHECK (order_amount >= 0),
                delivery_fee REAL NOT NULL CHECK (delivery_fee >= 0),

                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK (
                        status IN (
                            'Pending',
                            'Assigned',
                            'Out for Delivery',
                            'Delivered',
                            'Cancelled'
                        )
                    ),

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id),

                FOREIGN KEY (rider_id)
                    REFERENCES riders(rider_id)
            )
        """)

        connection.commit()

        print("Database tables created successfully!")

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# RUN DATABASE INITIALIZATION
# ==========================================

if __name__ == "__main__":
    create_tables()