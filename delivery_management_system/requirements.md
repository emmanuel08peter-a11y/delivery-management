# Local Delivery Order & Dispatch Management System

## 1. Project Overview

The Local Delivery Order & Dispatch Management System
is a Python desktop application designed to help small
delivery businesses manage customers, delivery orders,
delivery riders, and order statuses.

The system will use Python, Tkinter, SQLite, and SQL.

## 2. Project Objectives

The objectives of this project are to:

- Manage customer information.
- Create and manage delivery orders.
- Register and manage delivery riders.
- Assign riders to delivery orders.
- Track the progress of deliveries.
- Calculate delivery fees and order totals.
- Search for and filter orders.
- Generate basic delivery reports.
- Export order records to CSV.
- Store information in a database.

## 3. Functional Requirements

### 3.1 Customer Management

The system shall allow users to:

- Register new customers.
- Store customer names, phone numbers, and addresses.
- View customer information.
- Search for customers.

### 3.2 Order Management

The system shall allow users to:

- Create new delivery orders.
- Record the pickup and delivery addresses.
- Enter order descriptions and amounts.
- Calculate delivery fees.
- Calculate the total order cost.
- View existing orders.
- Search for orders by order ID or customer.
- Cancel orders when necessary.

### 3.3 Delivery Rider Management

The system shall allow users to:

- Register delivery riders.
- Store rider names and phone numbers.
- View registered riders.
- Assign riders to delivery orders.

### 3.4 Delivery Status Management

The system shall support these order statuses:

- Pending
- Assigned
- Out for Delivery
- Delivered
- Cancelled

Users shall be able to update order statuses
as deliveries progress.

### 3.5 Dashboard and Reports

The system shall display:

- Total number of orders.
- Number of pending orders.
- Number of delivered orders.
- Number of cancelled orders.
- Total delivery fees collected from completed deliveries.

### 3.6 Database Management

The system shall use SQLite to store:

- Customer records.
- Delivery rider records.
- Delivery order records.

The information shall remain available after
the application is closed.

### 3.7 CSV Export

The system shall allow users to export order
records into a CSV file for reporting purposes.

## 4. Non-Functional Requirements

### 4.1 Usability

The application should have a simple graphical
interface that is easy to understand.

### 4.2 Reliability

The system should validate user input and
handle common errors appropriately.

### 4.3 Data Persistence

Records shall be stored in an SQLite database
so they are not lost when the application closes.

### 4.4 Maintainability

The code shall be organized into separate files
for the interface, database operations, and models.

### 4.5 Performance

The system should efficiently handle the
customer, rider, and order records expected
in a small delivery business.

## 5. Technologies

- Python
- Object-Oriented Programming (OOP)
- Tkinter
- SQLite
- SQL
- CSV
- Git
- GitHub

## 6. Project Scope

This project focuses on managing local delivery
operations for a small delivery business.

The application will run as desktop software.

Online payments, GPS tracking, and live maps
are outside the initial project scope.