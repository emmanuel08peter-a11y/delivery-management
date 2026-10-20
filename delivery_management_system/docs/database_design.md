# Database Design

## 1. Introduction

The Local Delivery Order & Dispatch Management System
will use SQLite to store and manage information.

The database will contain three main tables:
Customers, Riders, and Orders.

## 2. Customers Table

This table stores customer information.

| Field | Data Type | Description |
|---|---|---|
| customer_id | INTEGER | Unique customer ID |
| name | TEXT | Customer's full name |
| phone | TEXT | Customer's phone number |
| address | TEXT | Customer's address |

The customer_id field will be the primary key.

## 3. Riders Table

This table stores delivery rider information.

| Field | Data Type | Description |
|---|---|---|
| rider_id | INTEGER | Unique rider ID |
| name | TEXT | Rider's full name |
| phone | TEXT | Rider's phone number |

The rider_id field will be the primary key.

## 4. Orders Table

This table stores delivery order information.

| Field | Data Type | Description |
|---|---|---|
| order_id | INTEGER | Unique order ID |
| customer_id | INTEGER | ID of the customer |
| rider_id | INTEGER | ID of the assigned rider |
| pickup_address | TEXT | Package pickup location |
| delivery_address | TEXT | Package destination |
| description | TEXT | Description of the package |
| order_amount | REAL | Value of the order |
| delivery_fee | REAL | Delivery charge |
| status | TEXT | Current delivery status |
| created_at | TEXT | Date and time the order was created |

The order_id field will be the primary key.

The customer_id field references the Customers table.

The rider_id field references the Riders table.
It may be empty until a rider is assigned.

## 5. Relationships

One customer can have multiple orders.

One rider can be assigned to multiple orders
over time.

Each order belongs to one customer.

An order may have one assigned rider or no rider
until an assignment is made.

## 6. Database Technology

SQLite will be used because it is lightweight,
does not require a separate database server,
and works well with Python applications.