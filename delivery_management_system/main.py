import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from database import create_tables, get_connection
from models import Customer, Rider, Order

# Application colours
PRIMARY_COLOR = "#1976D2"
BUTTON_TEXT_COLOR = "#FFFFFF"
BACK_BUTTON_COLOR = "#D3D3D3"
BACK_TEXT_COLOR = "#000000"
BACKGROUND_COLOR = "#F5F7FA"

APP_TITLE = "Local Delivery Order & Dispatch Management System"

ORDER_STATUSES = [
    "Pending",
    "Assigned",
    "Out for Delivery",
    "Delivered",
    "Cancelled"
]


def money(amount):
    return f"\u20a6{float(amount):,.2f}"


def open_database():
    """
    Use the existing database connection while allowing
    database records to be accessed by column name.
    """
    connection = get_connection()
    connection.row_factory = __import__("sqlite3").Row
    return connection


class DeliveryApp:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1100x680")
        self.root.minsize(850, 550)

        self.setup_style()
        self.build_dashboard()

# ==================================================
    # APPLICATION STYLE
    # ==================================================

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Main application buttons: blue with white text
        style.configure(
            "TButton",
            background=PRIMARY_COLOR,
            foreground=BUTTON_TEXT_COLOR,
            padding=8,
            font=("Arial", 10)
        )

        style.map(
            "TButton",
            background=[
                ("active", "#1565C0"),
                ("pressed", "#0D47A1"),
                ("disabled", "#B0BEC5")
            ],
            foreground=[
                ("disabled", "#EEEEEE")
            ]
        )

        # Back buttons: grey with black text
        style.configure(
            "Back.TButton",
            background=BACK_BUTTON_COLOR,
            foreground=BACK_TEXT_COLOR,
            padding=8,
            font=("Arial", 10)
        )

        style.map(
            "Back.TButton",
            background=[
                ("active", "#BDBDBD"),
                ("pressed", "#9E9E9E")
            ],
            foreground=[
                ("active", BACK_TEXT_COLOR)
            ]
        )

        # Application background
        style.configure(
            "TFrame",
            background=BACKGROUND_COLOR
        )

        # Normal labels
        style.configure(
            "TLabel",
            background=BACKGROUND_COLOR,
            foreground="#263238",
            font=("Arial", 10)
        )

        # Main headings
        style.configure(
            "Title.TLabel",
            background=BACKGROUND_COLOR,
            foreground="#1565C0",
            font=("Arial", 18, "bold")
        )

        # Smaller headings
        style.configure(
            "Heading.TLabel",
            background=BACKGROUND_COLOR,
            foreground="#263238",
            font=("Arial", 11, "bold")
        )

        # Table appearance
        style.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#BBDEFB")],
            foreground=[("selected", "#000000")]
        )
    # ==================================================
    # MAIN DASHBOARD
    # ==================================================

    def build_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=25)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text=APP_TITLE,
            style="Title.TLabel",
            wraplength=950
        ).pack(pady=(25, 12))

        ttk.Label(
            frame,
            text=(
                "Manage customers, riders, delivery orders, "
                "delivery statuses, and reports."
            ),
            wraplength=850
        ).pack(pady=(0, 25))

        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack()

        buttons = [
            ("Manage Customers", self.open_customers),
            ("Manage Riders", self.open_riders),
            ("Manage Orders", self.open_orders),
            ("View Reports", self.open_reports)
        ]

        for index, (label, command) in enumerate(buttons):
            ttk.Button(
                buttons_frame,
                text=label,
                command=command,
                width=28
            ).grid(
                row=index // 2,
                column=index % 2,
                padx=12,
                pady=12,
                sticky="ew"
            )

        summary_frame = ttk.LabelFrame(
            frame,
            text="System Summary",
            padding=15
        )
        summary_frame.pack(fill="x", pady=25)

        self.summary_label = ttk.Label(
            summary_frame,
            text=""
        )
        self.summary_label.pack()

        ttk.Button(
            frame,
            text="Refresh Summary",
            command=self.refresh_summary
        ).pack()

        self.refresh_summary()

    def refresh_summary(self):
        try:
            with open_database() as connection:

                customers = connection.execute(
                    "SELECT COUNT(*) FROM customers"
                ).fetchone()[0]

                riders = connection.execute(
                    "SELECT COUNT(*) FROM riders"
                ).fetchone()[0]

                orders = connection.execute(
                    "SELECT COUNT(*) FROM orders"
                ).fetchone()[0]

                active_orders = connection.execute("""
                    SELECT COUNT(*)
                    FROM orders
                    WHERE status IN (
                        'Pending',
                        'Assigned',
                        'Out for Delivery'
                    )
                """).fetchone()[0]

            self.summary_label.config(
                text=(
                    f"Customers: {customers}     "
                    f"Riders: {riders}     "
                    f"Total Orders: {orders}     "
                    f"Active Orders: {active_orders}"
                )
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self.root
            )

    def make_window(self, title, size="950x580"):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(size)
        window.transient(self.root)
        return window

    # ==================================================
    # CUSTOMER MANAGEMENT
    # ==================================================

    def open_customers(self):
        window = self.make_window(
            "Manage Customers",
            "950x580"
        )

        form = ttk.LabelFrame(
            window,
            text="Register Customer",
            padding=12
        )
        form.pack(fill="x", padx=12, pady=10)

        name_var = tk.StringVar()
        phone_var = tk.StringVar()
        address_var = tk.StringVar()

        ttk.Label(
            form,
            text="Full Name"
        ).grid(row=0, column=0, sticky="w", padx=4)

        ttk.Entry(
            form,
            textvariable=name_var,
            width=25
        ).grid(row=1, column=0, padx=4, pady=5)

        ttk.Label(
            form,
            text="Phone Number"
        ).grid(row=0, column=1, sticky="w", padx=4)

        ttk.Entry(
            form,
            textvariable=phone_var,
            width=20
        ).grid(row=1, column=1, padx=4, pady=5)

        ttk.Label(
            form,
            text="Address"
        ).grid(row=0, column=2, sticky="w", padx=4)

        ttk.Entry(
            form,
            textvariable=address_var,
            width=35
        ).grid(row=1, column=2, padx=4, pady=5)

        columns = (
            "id",
            "name",
            "phone",
            "address"
        )

        tree = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        headings = [
            ("id", "Customer ID", 100),
            ("name", "Customer Name", 200),
            ("phone", "Phone Number", 160),
            ("address", "Address", 400)
        ]

        for column, heading, width in headings:
            tree.heading(column, text=heading)
            tree.column(column, width=width, anchor="w")

        tree.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )

        def refresh():
            tree.delete(*tree.get_children())

            with open_database() as connection:
                records = connection.execute("""
                    SELECT customer_id, name, phone, address
                    FROM customers
                    ORDER BY customer_id DESC
                """).fetchall()

            for record in records:
                tree.insert(
                    "",
                    "end",
                    values=(
                        record["customer_id"],
                        record["name"],
                        record["phone"],
                        record["address"]
                    )
                )

        def register_customer():
            try:
                customer = Customer(
                    name_var.get(),
                    phone_var.get(),
                    address_var.get()
                )

                customer.save()

                messagebox.showinfo(
                    "Success",
                    "Customer registered successfully.",
                    parent=window
                )

                name_var.set("")
                phone_var.set("")
                address_var.set("")

                refresh()
                self.refresh_summary()

            except Exception as error:
                messagebox.showerror(
                    "Registration Error",
                    str(error),
                    parent=window
                )

        ttk.Button(
            form,
            text="Register Customer",
            command=register_customer
        ).grid(row=1, column=3, padx=8)

        ttk.Button(
            window,
            text="Refresh Customer List",
            command=refresh
        ).pack(pady=5)

        refresh()

    # ==================================================
    # RIDER MANAGEMENT
    # ==================================================

    def open_riders(self):
        window = self.make_window(
            "Manage Riders",
            "850x550"
        )

        form = ttk.LabelFrame(
            window,
            text="Register Delivery Rider",
            padding=12
        )
        form.pack(fill="x", padx=12, pady=10)

        name_var = tk.StringVar()
        phone_var = tk.StringVar()

        ttk.Label(
            form,
            text="Rider Name"
        ).grid(row=0, column=0, sticky="w", padx=4)

        ttk.Entry(
            form,
            textvariable=name_var,
            width=30
        ).grid(row=1, column=0, padx=4, pady=5)

        ttk.Label(
            form,
            text="Phone Number"
        ).grid(row=0, column=1, sticky="w", padx=4)

        ttk.Entry(
            form,
            textvariable=phone_var,
            width=25
        ).grid(row=1, column=1, padx=4, pady=5)

        columns = (
            "id",
            "name",
            "phone"
        )

        tree = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        tree.heading("id", text="Rider ID")
        tree.heading("name", text="Rider Name")
        tree.heading("phone", text="Phone Number")

        tree.column("id", width=100)
        tree.column("name", width=300)
        tree.column("phone", width=200)

        tree.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )

        def refresh():
            tree.delete(*tree.get_children())

            with open_database() as connection:
                records = connection.execute("""
                    SELECT rider_id, name, phone
                    FROM riders
                    ORDER BY rider_id DESC
                """).fetchall()

            for record in records:
                tree.insert(
                    "",
                    "end",
                    values=(
                        record["rider_id"],
                        record["name"],
                        record["phone"]
                    )
                )

        def register_rider():
            try:
                rider = Rider(
                    name_var.get(),
                    phone_var.get()
                )

                rider.save()

                messagebox.showinfo(
                    "Success",
                    "Rider registered successfully.",
                    parent=window
                )

                name_var.set("")
                phone_var.set("")

                refresh()
                self.refresh_summary()

            except Exception as error:
                messagebox.showerror(
                    "Registration Error",
                    str(error),
                    parent=window
                )

        ttk.Button(
            form,
            text="Register Rider",
            command=register_rider
        ).grid(row=1, column=2, padx=8)

        ttk.Button(
            window,
            text="Refresh Rider List",
            command=refresh
        ).pack(pady=5)

        refresh()

    # ==================================================
    # ORDER MANAGEMENT
    # ==================================================

    def open_orders(self):
        window = self.make_window(
            "Manage Orders",
            "1200x680"
        )

        form = ttk.LabelFrame(
            window,
            text="Create Delivery Order",
            padding=10
        )
        form.pack(fill="x", padx=10, pady=8)

        customer_var = tk.StringVar()
        pickup_var = tk.StringVar()
        delivery_var = tk.StringVar()
        description_var = tk.StringVar()
        amount_var = tk.StringVar()
        fee_var = tk.StringVar(value="0")
        total_var = tk.StringVar(value="Total: ₦0.00")

        customer_box = ttk.Combobox(
            form,
            textvariable=customer_var,
            state="readonly",
            width=25
        )

        ttk.Label(
            form,
            text="Customer"
        ).grid(row=0, column=0, sticky="w", padx=3)

        customer_box.grid(
            row=1,
            column=0,
            padx=3,
            pady=4
        )

        fields = [
            ("Pickup Address", pickup_var, 20),
            ("Delivery Address", delivery_var, 20),
            ("Item Description", description_var, 18),
            ("Order Amount", amount_var, 12),
            ("Delivery Fee", fee_var, 12)
        ]

        for index, (label, variable, width) in enumerate(
            fields,
            start=1
        ):
            ttk.Label(
                form,
                text=label
            ).grid(
                row=0,
                column=index,
                sticky="w",
                padx=3
            )

            ttk.Entry(
                form,
                textvariable=variable,
                width=width
            ).grid(
                row=1,
                column=index,
                padx=3,
                pady=4
            )

        ttk.Label(
            form,
            textvariable=total_var,
            style="Heading.TLabel"
        ).grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="w",
            padx=4,
            pady=5
        )

        def load_customers():
            with open_database() as connection:
                customers = connection.execute("""
                    SELECT customer_id, name, phone
                    FROM customers
                    ORDER BY name
                """).fetchall()

            customer_box["values"] = [
                f"{row['customer_id']} - {row['name']} ({row['phone']})"
                for row in customers
            ]

        def calculate_total(*args):
            try:
                amount = float(amount_var.get() or 0)
                fee = float(fee_var.get() or 0)

                total_var.set(
                    f"Total: {money(amount + fee)}"
                )

            except ValueError:
                total_var.set(
                    "Total: enter valid amounts"
                )

        amount_var.trace_add(
            "write",
            calculate_total
        )

        fee_var.trace_add(
            "write",
            calculate_total
        )

        columns = (
            "id",
            "customer",
            "rider",
            "pickup",
            "delivery",
            "description",
            "amount",
            "fee",
            "total",
            "status",
            "created"
        )

        tree = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        headings = [
            ("id", "Order ID", 65),
            ("customer", "Customer", 120),
            ("rider", "Rider", 100),
            ("pickup", "Pickup Address", 125),
            ("delivery", "Delivery Address", 125),
            ("description", "Description", 120),
            ("amount", "Order Amount", 95),
            ("fee", "Delivery Fee", 85),
            ("total", "Total", 90),
            ("status", "Status", 115),
            ("created", "Created At", 130)
        ]

        for column, heading, width in headings:
            tree.heading(column, text=heading)
            tree.column(
                column,
                width=width,
                anchor="w"
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=8
        )

        def refresh():
            tree.delete(*tree.get_children())

            with open_database() as connection:
                records = connection.execute("""
                    SELECT
                        o.order_id,
                        c.name AS customer,
                        COALESCE(r.name, 'Unassigned') AS rider,
                        o.pickup_address,
                        o.delivery_address,
                        o.description,
                        o.order_amount,
                        o.delivery_fee,
                        o.status,
                        o.created_at
                    FROM orders o
                    JOIN customers c
                        ON c.customer_id = o.customer_id
                    LEFT JOIN riders r
                        ON r.rider_id = o.rider_id
                    ORDER BY o.order_id DESC
                """).fetchall()

            for row in records:
                total = (
                    float(row["order_amount"])
                    + float(row["delivery_fee"])
                )

                tree.insert(
                    "",
                    "end",
                    values=(
                        row["order_id"],
                        row["customer"],
                        row["rider"],
                        row["pickup_address"],
                        row["delivery_address"],
                        row["description"],
                        money(row["order_amount"]),
                        money(row["delivery_fee"]),
                        money(total),
                        row["status"],
                        row["created_at"]
                    )
                )

        def create_order():
            try:
                if not customer_var.get():
                    raise ValueError(
                        "Register a customer and select them first."
                    )

                customer_id = int(
                    customer_var.get().split(" - ", 1)[0]
                )

                amount = float(amount_var.get())
                fee = float(fee_var.get())

                if amount < 0 or fee < 0:
                    raise ValueError(
                        "Amounts cannot be negative."
                    )

                order = Order(
                    customer_id,
                    pickup_var.get(),
                    delivery_var.get(),
                    description_var.get(),
                    amount,
                    fee
                )

                order.save()

                messagebox.showinfo(
                    "Success",
                    "Delivery order created successfully.",
                    parent=window
                )

                pickup_var.set("")
                delivery_var.set("")
                description_var.set("")
                amount_var.set("")
                fee_var.set("0")

                refresh()
                self.refresh_summary()

            except Exception as error:
                messagebox.showerror(
                    "Order Error",
                    str(error),
                    parent=window
                )

        def get_selected_order_id():
            selection = tree.selection()

            if not selection:
                messagebox.showwarning(
                    "No Order Selected",
                    "Select an order from the table first.",
                    parent=window
                )
                return None

            values = tree.item(
                selection[0],
                "values"
            )

            return int(values[0])

        def assign_rider():
            order_id = get_selected_order_id()

            if order_id is None:
                return

            with open_database() as connection:
                order_row = connection.execute(
                    "SELECT status FROM orders WHERE order_id = ?",
                    (order_id,)
                ).fetchone()

                riders = connection.execute("""
                    SELECT rider_id, name, phone
                    FROM riders
                    ORDER BY name
                """).fetchall()

            if not riders:
                messagebox.showwarning(
                    "No Riders",
                    "Register a rider before assigning one.",
                    parent=window
                )
                return

            if order_row["status"] in (
                "Delivered",
                "Cancelled"
            ):
                messagebox.showwarning(
                    "Cannot Assign",
                    "Delivered or cancelled orders cannot be reassigned.",
                    parent=window
                )
                return

            picker = tk.Toplevel(window)
            picker.title("Assign Rider")
            picker.geometry("380x160")
            picker.transient(window)

            ttk.Label(
                picker,
                text="Select a delivery rider"
            ).pack(pady=(15, 5))

            options = [
                f"{rider['rider_id']} - {rider['name']} ({rider['phone']})"
                for rider in riders
            ]

            rider_var = tk.StringVar(
                value=options[0]
            )

            ttk.Combobox(
                picker,
                textvariable=rider_var,
                values=options,
                state="readonly",
                width=40
            ).pack(padx=10, pady=5)

            def save_assignment():
                try:
                    rider_id = int(
                        rider_var.get().split(" - ", 1)[0]
                    )

                    with open_database() as connection:
                        connection.execute("""
                            UPDATE orders
                            SET rider_id = ?, status = 'Assigned'
                            WHERE order_id = ?
                        """, (rider_id, order_id))

                    picker.destroy()
                    refresh()
                    self.refresh_summary()

                    messagebox.showinfo(
                        "Success",
                        "Rider assigned successfully.",
                        parent=window
                    )

                except Exception as error:
                    messagebox.showerror(
                        "Assignment Error",
                        str(error),
                        parent=picker
                    )

            ttk.Button(
                picker,
                text="Assign Rider",
                command=save_assignment
            ).pack(pady=8)

        def update_status():
            order_id = get_selected_order_id()

            if order_id is None:
                return

            with open_database() as connection:
                row = connection.execute("""
                    SELECT status, rider_id
                    FROM orders
                    WHERE order_id = ?
                """, (order_id,)).fetchone()

            if row["status"] in (
                "Delivered",
                "Cancelled"
            ):
                messagebox.showwarning(
                    "Cannot Update",
                    "Delivered and cancelled orders are final.",
                    parent=window
                )
                return

            picker = tk.Toplevel(window)
            picker.title("Update Delivery Status")
            picker.geometry("350x170")
            picker.transient(window)

            ttk.Label(
                picker,
                text="Select the new delivery status"
            ).pack(pady=(15, 5))

            status_var = tk.StringVar(
                value=row["status"]
            )

            ttk.Combobox(
                picker,
                textvariable=status_var,
                values=ORDER_STATUSES,
                state="readonly",
                width=28
            ).pack(pady=5)

            def save_status():
                new_status = status_var.get()

                if (
                    new_status in (
                        "Assigned",
                        "Out for Delivery"
                    )
                    and row["rider_id"] is None
                ):
                    messagebox.showerror(
                        "Rider Required",
                        "Assign a rider before using this status.",
                        parent=picker
                    )
                    return

                try:
                    with open_database() as connection:
                        connection.execute("""
                            UPDATE orders
                            SET status = ?
                            WHERE order_id = ?
                        """, (new_status, order_id))

                    picker.destroy()
                    refresh()
                    self.refresh_summary()

                except Exception as error:
                    messagebox.showerror(
                        "Status Error",
                        str(error),
                        parent=picker
                    )

            ttk.Button(
                picker,
                text="Save Status",
                command=save_status
            ).pack(pady=8)

        def cancel_order():
            order_id = get_selected_order_id()

            if order_id is None:
                return

            confirmed = messagebox.askyesno(
                "Cancel Order",
                f"Are you sure you want to cancel order #{order_id}?",
                parent=window
            )

            if not confirmed:
                return

            with open_database() as connection:
                row = connection.execute(
                    "SELECT status FROM orders WHERE order_id = ?",
                    (order_id,)
                ).fetchone()

                if row["status"] == "Delivered":
                    messagebox.showwarning(
                        "Cannot Cancel",
                        "A delivered order cannot be cancelled.",
                        parent=window
                    )
                    return

                connection.execute("""
                    UPDATE orders
                    SET status = 'Cancelled'
                    WHERE order_id = ?
                """, (order_id,))

            refresh()
            self.refresh_summary()

            messagebox.showinfo(
                "Order Cancelled",
                f"Order #{order_id} has been cancelled.",
                parent=window
            )

        ttk.Button(
            form,
            text="Create Order",
            command=create_order
        ).grid(
            row=2,
            column=5,
            padx=5,
            pady=5
        )

        action_frame = ttk.Frame(window)
        action_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        actions = [
            ("Refresh Orders", refresh),
            ("Assign Rider", assign_rider),
            ("Update Status", update_status),
            ("Cancel Order", cancel_order)
        ]

        for label, command in actions:
            ttk.Button(
                action_frame,
                text=label,
                command=command
            ).pack(
                side="left",
                padx=5
            )

        load_customers()
        refresh()

    # ==================================================
    # REPORTS AND CSV EXPORT
    # ==================================================

    def open_reports(self):
        window = self.make_window(
            "Reports and CSV Export",
            "1050x600"
        )

        ttk.Label(
            window,
            text="Order and Revenue Reports",
            style="Title.TLabel"
        ).pack(pady=12)

        summary_frame = ttk.LabelFrame(
            window,
            text="Report Summary",
            padding=12
        )
        summary_frame.pack(
            fill="x",
            padx=12,
            pady=8
        )

        summary_label = ttk.Label(
            summary_frame,
            text=""
        )
        summary_label.pack(anchor="w")

        columns = (
            "id",
            "customer",
            "status",
            "amount",
            "fee",
            "total",
            "created"
        )

        tree = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        headings = [
            ("id", "Order ID", 80),
            ("customer", "Customer", 200),
            ("status", "Status", 140),
            ("amount", "Order Amount", 130),
            ("fee", "Delivery Fee", 120),
            ("total", "Total Amount", 130),
            ("created", "Created At", 170)
        ]

        for column, heading, width in headings:
            tree.heading(column, text=heading)
            tree.column(
                column,
                width=width,
                anchor="w"
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=8
        )

        def refresh_reports():
            tree.delete(*tree.get_children())

            with open_database() as connection:
                records = connection.execute("""
                    SELECT
                        o.order_id,
                        c.name AS customer,
                        o.status,
                        o.order_amount,
                        o.delivery_fee,
                        o.created_at
                    FROM orders o
                    JOIN customers c
                        ON c.customer_id = o.customer_id
                    ORDER BY o.order_id DESC
                """).fetchall()

                total_orders = connection.execute("""
                    SELECT COUNT(*)
                    FROM orders
                    WHERE status <> 'Cancelled'
                """).fetchone()[0]

                delivered_orders = connection.execute("""
                    SELECT COUNT(*)
                    FROM orders
                    WHERE status = 'Delivered'
                """).fetchone()[0]

                revenue = connection.execute("""
                    SELECT COALESCE(
                        SUM(order_amount + delivery_fee), 0
                    )
                    FROM orders
                    WHERE status = 'Delivered'
                """).fetchone()[0]

                today_orders = connection.execute("""
                    SELECT COUNT(*)
                    FROM orders
                    WHERE date(created_at) = date('now', 'localtime')
                    AND status <> 'Cancelled'
                """).fetchone()[0]

                monthly_orders = connection.execute("""
                    SELECT COUNT(*)
                    FROM orders
                    WHERE strftime('%Y-%m', created_at)
                        = strftime('%Y-%m', 'now', 'localtime')
                    AND status <> 'Cancelled'
                """).fetchone()[0]

            summary_label.config(
                text=(
                    f"Valid Orders: {total_orders}     "
                    f"Delivered Orders: {delivered_orders}     "
                    f"Delivered Revenue: {money(revenue)}     "
                    f"Today's Orders: {today_orders}     "
                    f"This Month's Orders: {monthly_orders}"
                )
            )

            for row in records:
                total = (
                    float(row["order_amount"])
                    + float(row["delivery_fee"])
                )

                tree.insert(
                    "",
                    "end",
                    values=(
                        row["order_id"],
                        row["customer"],
                        row["status"],
                        money(row["order_amount"]),
                        money(row["delivery_fee"]),
                        money(total),
                        row["created_at"]
                    )
                )

        def export_csv():
            path = filedialog.asksaveasfilename(
                parent=window,
                title="Save Orders Report",
                defaultextension=".csv",
                filetypes=[
                    ("CSV Files", "*.csv")
                ]
            )

            if not path:
                return

            try:
                with open_database() as connection:
                    records = connection.execute("""
                        SELECT
                            o.order_id,
                            c.name AS customer_name,
                            c.phone AS customer_phone,
                            o.pickup_address,
                            o.delivery_address,
                            o.description,
                            o.order_amount,
                            o.delivery_fee,
                            (
                                o.order_amount + o.delivery_fee
                            ) AS total_amount,
                            COALESCE(r.name, 'Unassigned') AS rider_name,
                            o.status,
                            o.created_at
                        FROM orders o
                        JOIN customers c
                            ON c.customer_id = o.customer_id
                        LEFT JOIN riders r
                            ON r.rider_id = o.rider_id
                        ORDER BY o.order_id
                    """).fetchall()

                with open(
                    path,
                    "w",
                    newline="",
                    encoding="utf-8-sig"
                ) as file:
                    writer = csv.writer(file)

                    writer.writerow([
                        "Order ID",
                        "Customer Name",
                        "Customer Phone",
                        "Pickup Address",
                        "Delivery Address",
                        "Description",
                        "Order Amount",
                        "Delivery Fee",
                        "Total Amount",
                        "Rider",
                        "Status",
                        "Created At"
                    ])

                    for record in records:
                        writer.writerow(tuple(record))

                messagebox.showinfo(
                    "Export Successful",
                    f"Orders exported successfully to:\n{path}",
                    parent=window
                )

            except Exception as error:
                messagebox.showerror(
                    "Export Error",
                    str(error),
                    parent=window
                )

        buttons_frame = ttk.Frame(window)
        buttons_frame.pack(pady=(0, 10))

        ttk.Button(
            buttons_frame,
            text="Refresh Reports",
            command=refresh_reports
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="Export Orders to CSV",
            command=export_csv
        ).pack(side="left", padx=5)

        refresh_reports()


# ======================================================
# START APPLICATION
# ======================================================

def main():
    create_tables()

    root = tk.Tk()
    DeliveryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()