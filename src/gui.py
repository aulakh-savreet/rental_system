import tkinter as tk
from tkinter import ttk, messagebox
from models import Equipment, Customer, Rental, Category
from data_manager import (
    get_categories, add_category,
    get_equipment, add_equipment, delete_equipment,
    get_customers, add_customer, delete_customer,
    get_rentals, add_rental, generate_rental_id,
    get_equipment_by_id
)
import datetime

class RentalAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Equipment Rental System")
        self.root.geometry("900x600")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=6, relief='flat', background='#ccc')
        style.configure('TLabel', background='#eee', padding=4)
        style.configure('TFrame', background='#eee')

        self.create_menu()
        self.create_notebook()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def show_about(self):
        messagebox.showinfo("About", "Equipment Rental System Prototype")

    def create_notebook(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        equipment_frame = ttk.Frame(notebook)
        customers_frame = ttk.Frame(notebook)
        rentals_frame = ttk.Frame(notebook)

        notebook.add(equipment_frame, text="Equipment")
        notebook.add(customers_frame, text="Customers")
        notebook.add(rentals_frame, text="Rentals")

        self.create_equipment_tab(equipment_frame)
        self.create_customers_tab(customers_frame)
        self.create_rentals_tab(rentals_frame)

    def create_equipment_tab(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        ttk.Label(action_frame, text="Manage Equipment", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=10)

        add_eq_btn = ttk.Button(action_frame, text="Add Equipment", command=self.open_add_equipment_window)
        add_eq_btn.pack(side=tk.LEFT, padx=5)

        del_eq_btn = ttk.Button(action_frame, text="Delete Selected", command=self.delete_selected_equipment)
        del_eq_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(action_frame, text="Refresh List", command=self.refresh_equipment_tree)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        columns = ("ID", "Name", "Category ID", "Description", "Daily Rate", "Available")
        self.equipment_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        for col in columns:
            self.equipment_tree.heading(col, text=col)
            self.equipment_tree.column(col, width=120)
        self.equipment_tree.pack(expand=True, fill='both')

        self.refresh_equipment_tree()

    def refresh_equipment_tree(self):
        for i in self.equipment_tree.get_children():
            self.equipment_tree.delete(i)
        equipment_list = get_equipment()
        for eq in equipment_list:
            self.equipment_tree.insert('', tk.END, values=(
                eq.equipment_id,
                eq.name,
                eq.category_id,
                eq.description,
                f"${eq.daily_rate:.2f}" if eq.daily_rate else "N/A",
                "Yes" if eq.available else "No"
            ))

    def open_add_equipment_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Equipment")
        win.geometry("400x400")

        def add_equipment_action():
            try:
                equipment_id = int(entry_id.get())
            except ValueError:
                messagebox.showerror("Error", "Equipment ID must be an integer.")
                return

            cat_id_str = entry_cat_id.get().strip()
            if not cat_id_str.isdigit():
                messagebox.showerror("Error", "Category ID must be an integer.")
                return
            category_id = int(cat_id_str)

            name = entry_name.get().strip()
            if not name:
                messagebox.showerror("Error", "Name cannot be empty.")
                return

            description = entry_desc.get("1.0", tk.END).strip()
            try:
                daily_rate = float(entry_rate.get()) if entry_rate.get() else 0.0
            except ValueError:
                daily_rate = 0.0

            contact_phone = entry_phone.get().strip()
            email = entry_email.get().strip()

            eq = Equipment(
                equipment_id=equipment_id,
                category_id=category_id,
                name=name,
                description=description,
                daily_rate=daily_rate,
                contact_phone=contact_phone,
                email=email,
                available=True
            )

            success, msg = add_equipment(eq)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_equipment_tree()
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        form_frame = ttk.Frame(win)
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Equipment ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_id = ttk.Entry(form_frame)
        entry_id.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Category ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_cat_id = ttk.Entry(form_frame)
        entry_cat_id.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_name = ttk.Entry(form_frame)
        entry_name.grid(row=2, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_desc = tk.Text(form_frame, height=4, width=20)
        entry_desc.grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Daily Rate:").grid(row=4, column=0, sticky=tk.W, pady=5)
        entry_rate = ttk.Entry(form_frame)
        entry_rate.grid(row=4, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Contact Phone:").grid(row=5, column=0, sticky=tk.W, pady=5)
        entry_phone = ttk.Entry(form_frame)
        entry_phone.grid(row=5, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=6, column=0, sticky=tk.W, pady=5)
        entry_email = ttk.Entry(form_frame)
        entry_email.grid(row=6, column=1, sticky=tk.EW, pady=5)

        add_btn = ttk.Button(form_frame, text="Add Equipment", command=add_equipment_action)
        add_btn.grid(row=7, column=0, columnspan=2, pady=10)

        for i in range(2):
            form_frame.columnconfigure(i, weight=1)

    def delete_selected_equipment(self):
        selected = self.equipment_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No equipment selected.")
            return
        item = self.equipment_tree.item(selected)
        equipment_id = item['values'][0]
        success, msg = delete_equipment(equipment_id)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_equipment_tree()
        else:
            messagebox.showerror("Error", msg)

    def create_customers_tab(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        ttk.Label(action_frame, text="Manage Customers", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=10)

        add_cust_btn = ttk.Button(action_frame, text="Add Customer", command=self.open_add_customer_window)
        add_cust_btn.pack(side=tk.LEFT, padx=5)

        del_cust_btn = ttk.Button(action_frame, text="Delete Selected", command=self.delete_selected_customer)
        del_cust_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(action_frame, text="Refresh List", command=self.refresh_customers_tree)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        columns = ("ID", "Last Name", "First Name", "Contact Phone", "Email")
        self.customers_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=120)
        self.customers_tree.pack(expand=True, fill='both')

        self.refresh_customers_tree()

    def refresh_customers_tree(self):
        for i in self.customers_tree.get_children():
            self.customers_tree.delete(i)
        customers = get_customers()
        for cl in customers:
            self.customers_tree.insert('', tk.END, values=(
                cl.customer_id,
                cl.last_name,
                cl.first_name,
                cl.contact_phone,
                cl.email
            ))

    def open_add_customer_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Customer")
        win.geometry("400x300")

        def add_customer_action():
            try:
                customer_id = int(entry_id.get())
            except ValueError:
                messagebox.showerror("Error", "Customer ID must be an integer.")
                return

            last_name = entry_last.get().strip()
            first_name = entry_first.get().strip()
            if not last_name or not first_name:
                messagebox.showerror("Error", "First and last names cannot be empty.")
                return
            phone = entry_phone.get().strip()
            email = entry_email.get().strip()

            cust = Customer(customer_id, last_name, first_name, phone, email)
            success, msg = add_customer(cust)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_customers_tree()
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        form_frame = ttk.Frame(win)
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_id = ttk.Entry(form_frame)
        entry_id.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_last = ttk.Entry(form_frame)
        entry_last.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="First Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_first = ttk.Entry(form_frame)
        entry_first.grid(row=2, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Phone:").grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_phone = ttk.Entry(form_frame)
        entry_phone.grid(row=3, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky=tk.W, pady=5)
        entry_email = ttk.Entry(form_frame)
        entry_email.grid(row=4, column=1, sticky=tk.EW, pady=5)

        add_btn = ttk.Button(form_frame, text="Add Customer", command=add_customer_action)
        add_btn.grid(row=5, column=0, columnspan=2, pady=10)

        for i in range(2):
            form_frame.columnconfigure(i, weight=1)

    def delete_selected_customer(self):
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No customer selected.")
            return
        item = self.customers_tree.item(selected)
        customer_id = item['values'][0]
        success, msg = delete_customer(customer_id)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_customers_tree()
        else:
            messagebox.showerror("Error", msg)

    def create_rentals_tab(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        ttk.Label(action_frame, text="Manage Rentals", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=10)

        add_rental_btn = ttk.Button(action_frame, text="Process Rental", command=self.open_add_rental_window)
        add_rental_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(action_frame, text="Refresh List", command=self.refresh_rentals_tree)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        columns = ("Rental ID", "Date", "Customer ID", "Equipment ID", "Return Date", "Cost")
        self.rentals_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        for col in columns:
            self.rentals_tree.heading(col, text=col)
            self.rentals_tree.column(col, width=120)
        self.rentals_tree.pack(expand=True, fill='both')

        self.refresh_rentals_tree()

    def refresh_rentals_tree(self):
        for i in self.rentals_tree.get_children():
            self.rentals_tree.delete(i)
        rentals = get_rentals()
        for rt in rentals:
            self.rentals_tree.insert('', tk.END, values=(
                rt.rental_id,
                rt.date,
                rt.customer_id,
                rt.equipment_id,
                rt.return_date,
                f"${rt.cost:.2f}"
            ))

    def open_add_rental_window(self):
        customers = get_customers()
        equipment_list = get_equipment()
        available_equipment = [eq for eq in equipment_list if eq.available]

        if not customers:
            messagebox.showerror("Error", "No customers available. Please add customers first.")
            return

        if not available_equipment:
            messagebox.showerror("Error", "No available equipment to rent.")
            return

        win = tk.Toplevel(self.root)
        win.title("Process Rental")
        win.geometry("400x400")

        customers_values = [f"{c.customer_id} - {c.first_name} {c.last_name}" for c in customers]
        equipment_values = [f"{e.equipment_id} - {e.name}" for e in available_equipment]

        form_frame = ttk.Frame(win)
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Customer:").grid(row=0, column=0, sticky=tk.W, pady=5)
        customer_var = tk.StringVar()
        customer_cb = ttk.Combobox(form_frame, textvariable=customer_var, values=customers_values, state="readonly")
        customer_cb.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Equipment:").grid(row=1, column=0, sticky=tk.W, pady=5)
        equipment_var = tk.StringVar()
        equipment_cb = ttk.Combobox(form_frame, textvariable=equipment_var, values=equipment_values, state="readonly")
        equipment_cb.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Rental Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        rental_date_entry = ttk.Entry(form_frame)
        rental_date_entry.insert(0, datetime.date.today().isoformat())
        rental_date_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Return Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=5)
        return_date_entry = ttk.Entry(form_frame)
        return_date_entry.insert(0, (datetime.date.today() + datetime.timedelta(days=1)).isoformat())
        return_date_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)

        cost_label = ttk.Label(form_frame, text="Cost: $0.00", font=('Arial', 12, 'bold'))
        cost_label.grid(row=4, column=0, columnspan=2, pady=10)

        def update_cost_display(*args):
            # Recalculate cost when dates or equipment change
            eq_id_str = equipment_var.get().split(" - ")[0] if equipment_var.get() else ""
            if not eq_id_str.isdigit():
                cost_label.config(text="Cost: $0.00")
                return
            equipment_id_val = int(eq_id_str)
            eq = get_equipment_by_id(equipment_id_val)
            if eq is None:
                cost_label.config(text="Cost: $0.00")
                return

            rental_date_str = rental_date_entry.get().strip()
            return_date_str = return_date_entry.get().strip()

            try:
                rental_date = datetime.datetime.strptime(rental_date_str, "%Y-%m-%d").date()
                return_date = datetime.datetime.strptime(return_date_str, "%Y-%m-%d").date()
                if return_date < rental_date:
                    cost_label.config(text="Cost: $0.00")
                    return
                days = (return_date - rental_date).days
                if days < 0:
                    days = 0
                cost = eq.daily_rate * days
                cost_label.config(text=f"Cost: ${cost:.2f}")
            except ValueError:
                # Invalid date format
                cost_label.config(text="Cost: $0.00")

        equipment_cb.bind('<<ComboboxSelected>>', update_cost_display)
        rental_date_entry.bind('<KeyRelease>', update_cost_display)
        return_date_entry.bind('<KeyRelease>', update_cost_display)

        def process_rental_action():
            if not customer_var.get() or not equipment_var.get():
                messagebox.showerror("Error", "Select both customer and equipment.")
                return

            rental_date_str = rental_date_entry.get().strip()
            return_date_str = return_date_entry.get().strip()

            if not rental_date_str or not return_date_str:
                messagebox.showerror("Error", "Enter both rental and return dates.")
                return

            try:
                rental_date = datetime.datetime.strptime(rental_date_str, "%Y-%m-%d").date()
                return_date = datetime.datetime.strptime(return_date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Dates must be in YYYY-MM-DD format.")
                return

            if return_date < rental_date:
                messagebox.showerror("Error", "Return date cannot be before rental date.")
                return

            customer_id = int(customer_var.get().split(" - ")[0])
            equipment_id = int(equipment_var.get().split(" - ")[0])

            eq = get_equipment_by_id(equipment_id)
            if eq is None:
                messagebox.showerror("Error", "Selected equipment not found.")
                return

            days = (return_date - rental_date).days
            cost = eq.daily_rate * days

            rental_id = generate_rental_id()
            rental = Rental(
                rental_id=rental_id,
                date=str(rental_date),
                customer_id=customer_id,
                equipment_id=equipment_id,
                return_date=str(return_date),
                cost=cost
            )

            success, msg = add_rental(rental)
            if success:
                messagebox.showinfo("Success", f"{msg}\nCost: ${cost:.2f}")
                self.refresh_rentals_tree()
                self.refresh_equipment_tree()
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        add_btn = ttk.Button(form_frame, text="Process Rental", command=process_rental_action)
        add_btn.grid(row=5, column=0, columnspan=2, pady=10)

        for i in range(2):
            form_frame.columnconfigure(i, weight=1)


