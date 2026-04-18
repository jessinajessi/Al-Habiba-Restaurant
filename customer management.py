import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

conn = sqlite3.connect("al_habiba.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT,
    email TEXT,
    address TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customer_purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    item TEXT,
    amount REAL,
    date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)
""")
conn.commit()

root = tk.Tk()
root.title("Al-Habiba Restaurant - Customer Management")
root.geometry("1000x650")
root.configure(bg="#ff8080")
label = tk.Label(root, text="Al-Habiba Restaurant", font=("Arial", 16, "bold"),
                 fg="#000099", bg="#00b3b3")
label.pack(pady=20)

frame_form = tk.LabelFrame(root, text="Customer Details", padx=10, pady=10, bg="#F8F9F9", font=('Arial', 12, 'bold'))
frame_form.pack(fill="x", padx=10, pady=5)

tk.Label(frame_form, text="Name:", bg="#F8F9F9").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Contact:", bg="#F8F9F9").grid(row=0, column=2, padx=5, pady=5)
tk.Label(frame_form, text="Email:", bg="#F8F9F9").grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Address:", bg="#F8F9F9").grid(row=1, column=2, padx=5, pady=5)

name_var = tk.StringVar()
contact_var = tk.StringVar()
email_var = tk.StringVar()
address_var = tk.StringVar()

tk.Entry(frame_form, textvariable=name_var, width=25).grid(row=0, column=1, padx=5, pady=5)
tk.Entry(frame_form, textvariable=contact_var, width=25).grid(row=0, column=3, padx=5, pady=5)
tk.Entry(frame_form, textvariable=email_var, width=25).grid(row=1, column=1, padx=5, pady=5)
tk.Entry(frame_form, textvariable=address_var, width=25).grid(row=1, column=3, padx=5, pady=5)

frame_btn = tk.Frame(root, bg="#F8F9F9")
frame_btn.pack(pady=5)

def clear_fields():
    name_var.set("")
    contact_var.set("")
    email_var.set("")
    address_var.set("")

def add_customer():
    name = name_var.get()
    contact = contact_var.get()
    email = email_var.get()
    address = address_var.get()

    if name == "":
        messagebox.showerror("Error", "Name is required!")
        return

    cursor.execute("INSERT INTO customers (name, contact, email, address) VALUES (?, ?, ?, ?)",
                   (name, contact, email, address))
    conn.commit()
    messagebox.showinfo("Success", "Customer added successfully!")
    show_customers()
    clear_fields()

def update_customer():
    selected = customer_table.focus()
    if not selected:
        messagebox.showwarning("Select Customer", "Please select a customer to update.")
        return
    customer_id = customer_table.item(selected)['values'][0]

    cursor.execute("UPDATE customers SET name=?, contact=?, email=?, address=? WHERE id=?",
                   (name_var.get(), contact_var.get(), email_var.get(), address_var.get(), customer_id))
    conn.commit()
    messagebox.showinfo("Updated", "Customer updated successfully!")
    show_customers()
    clear_fields()

def delete_customer():
    selected = customer_table.focus()
    if not selected:
        messagebox.showwarning("Select Customer", "Please select a customer to delete.")
        return
    customer_id = customer_table.item(selected)['values'][0]

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?")
    if confirm:
        cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
        cursor.execute("DELETE FROM customer_purchases WHERE customer_id=?", (customer_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Customer and their purchases deleted successfully!")
        show_customers()

tk.Button(frame_btn, text="Add Customer", command=add_customer, bg="#27AE60", fg="white", width=15).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="Update Customer", command=update_customer, bg="#2980B9", fg="white", width=15).grid(row=0, column=1, padx=10)
tk.Button(frame_btn, text="Delete Customer", command=delete_customer, bg="#E74C3C", fg="white", width=15).grid(row=0, column=2, padx=10)
tk.Button(frame_btn, text="Clear Fields", command=clear_fields, bg="#7F8C8D", fg="white", width=15).grid(row=0, column=3, padx=10)

frame_list = tk.LabelFrame(root, text="Customers List", bg="#F8F9F9", font=('Arial', 12, 'bold'))
frame_list.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Name", "Contact", "Email", "Address")
customer_table = ttk.Treeview(frame_list, columns=columns, show="headings", height=8)
for col in columns:
    customer_table.heading(col, text=col)
    customer_table.column(col, width=150)
customer_table.pack(fill="both", expand=True)

def show_customers():
    for row in customer_table.get_children():
        customer_table.delete(row)
    cursor.execute("SELECT * FROM customers")
    for customer in cursor.fetchall():
        customer_table.insert("", "end", values=customer)

def on_customer_select(event):
    selected = customer_table.focus()
    if selected:
        values = customer_table.item(selected, "values")
        name_var.set(values[1])
        contact_var.set(values[2])
        email_var.set(values[3])
        address_var.set(values[4])
        show_purchases(values[0])

customer_table.bind("<ButtonRelease-1>", on_customer_select)

frame_purchase = tk.LabelFrame(root, text="Customer Purchases", bg="#F8F9F9", font=('Arial', 12, 'bold'))
frame_purchase.pack(fill="both", expand=True, padx=10, pady=5)

tk.Label(frame_purchase, text="Item:", bg="#F8F9F9").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_purchase, text="Amount:", bg="#F8F9F9").grid(row=0, column=2, padx=5, pady=5)

item_var = tk.StringVar()
amount_var = tk.StringVar()

tk.Entry(frame_purchase, textvariable=item_var, width=25).grid(row=0, column=1, padx=5, pady=5)
tk.Entry(frame_purchase, textvariable=amount_var, width=25).grid(row=0, column=3, padx=5, pady=5)

def add_purchase():
    selected = customer_table.focus()
    if not selected:
        messagebox.showwarning("Select Customer", "Please select a customer first.")
        return
    customer_id = customer_table.item(selected)['values'][0]
    item = item_var.get()
    amount = amount_var.get()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if item == "" or amount == "":
        messagebox.showerror("Error", "Please fill all fields!")
        return

    cursor.execute("INSERT INTO customer_purchases (customer_id, item, amount, date) VALUES (?, ?, ?, ?)",
                   (customer_id, item, amount, date))
    conn.commit()
    messagebox.showinfo("Success", "Purchase recorded successfully!")
    show_purchases(customer_id)
    item_var.set("")
    amount_var.set("")

tk.Button(frame_purchase, text="Add Purchase", command=add_purchase, bg="#16A085", fg="white", width=20).grid(row=0, column=4, padx=10)

columns_p = ("ID", "Item", "Amount", "Date")
purchase_table = ttk.Treeview(frame_purchase, columns=columns_p, show="headings", height=6)
for col in columns_p:
    purchase_table.heading(col, text=col)
    purchase_table.column(col, width=150)
purchase_table.grid(row=1, column=0, columnspan=5, pady=10)

def show_purchases(customer_id):
    for row in purchase_table.get_children():
        purchase_table.delete(row)
    cursor.execute("SELECT id, item, amount, date FROM customer_purchases WHERE customer_id=?", (customer_id,))
    for purchase in cursor.fetchall():
        purchase_table.insert("", "end", values=purchase)

show_customers()

root.mainloop()
