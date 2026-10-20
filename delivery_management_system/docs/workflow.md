# System Workflow

## 1. Overview

This document describes how the Local Delivery Order
& Dispatch Management System operates.

## 2. Order Workflow

1. The delivery manager opens the application.
2. The manager registers a customer if necessary.
3. The manager enters the delivery order details.
4. The system validates the information.
5. The system calculates the delivery fee and total cost.
6. The order is saved in the SQLite database.
7. A delivery rider is assigned to the order.
8. The order status changes as the delivery progresses.
9. The manager marks the order as delivered or cancelled.
10. The dashboard updates its statistics.

## 3. Order Statuses

- Pending: The order has been created.
- Assigned: A rider has been assigned.
- Out for Delivery: The rider is delivering the package.
- Delivered: The delivery has been completed.
- Cancelled: The order has been cancelled.

## 4. Error Handling

If required information is missing or invalid,
the system should display an appropriate error message.

If a database operation fails, the system should
inform the user rather than crashing unexpectedly.