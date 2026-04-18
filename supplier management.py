import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

conn = sqlite3.connect("al_habiba.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT,
    email TEXT,
    address TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS supplier_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER,
    item TEXT,
    amount REAL,
    date TEXT,
    FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
)
""")
conn.commit()

root = tk.Tk()
root.title("Al-Habiba Restaurant - Supplier Management")
root.geometry("900x600")
root.configure(bg="#ff8080")
label = tk.Label(root, text="Al-Habiba Restaurant", font=("Arial", 16, "bold"),
                 fg="#000099", bg="#00b3b3")
label.pack(pady=20)


frame_form = tk.LabelFrame(root, text="Supplier Details", padx=10, pady=10, bg="#EAF0F1", font=('Arial', 12, 'bold'))
frame_form.pack(fill="x", padx=10, pady=5)

tk.Label(frame_form, text="Name:", bg="#EAF0F1").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Contact:", bg="#EAF0F1").grid(row=0, column=2, padx=5, pady=5)
tk.Label(frame_form, text="Email:", bg="#EAF0F1").grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Address:", bg="#EAF0F1").grid(row=1, column=2, padx=5, pady=5)

name_var = tk.StringVar()
contact_var = tk.StringVar()
email_var = tk.StringVar()
address_var = tk.StringVar()

name_entry = tk.Entry(frame_form, textvariable=name_var, width=25)
contact_entry = tk.Entry(frame_form, textvariable=contact_var, width=25)
email_entry = tk.Entry(frame_form, textvariable=email_var, width=25)
address_entry = tk.Entry(frame_form, textvariable=address_var, width=25)

name_entry.grid(row=0, column=1, padx=5, pady=5)
contact_entry.grid(row=0, column=3, padx=5, pady=5)
email_entry.grid(row=1, column=1, padx=5, pady=5)
address_entry.grid(row=1, column=3, padx=5, pady=5)

frame_btn = tk.Frame(root, bg="#EAF0F1")
frame_btn.pack(pady=5)

def clear_fields():
    name_var.set("")
    contact_var.set("")
    email_var.set("")
    address_var.set("")

def add_supplier():
    name = name_var.get()
    contact = contact_var.get()
    email = email_var.get()
    address = address_var.get()

    if name == "":
        messagebox.showerror("Error", "Name is required!")
        return

    cursor.execute("INSERT INTO suppliers (name, contact, email, address) VALUES (?, ?, ?, ?)",
                   (name, contact, email, address))
    conn.commit()
    messagebox.showinfo("Success", "Supplier added successfully!")
    show_suppliers()
    clear_fields()

def update_supplier():
    selected = supplier_table.focus()
    if not selected:
        messagebox.showwarning("Select Supplier", "Please select a supplier to update.")
        return
    supplier_id = supplier_table.item(selected)['values'][0]

    cursor.execute("UPDATE suppliers SET name=?, contact=?, email=?, address=? WHERE id=?",
                   (name_var.get(), contact_var.get(), email_var.get(), address_var.get(), supplier_id))
    conn.commit()
    messagebox.showinfo("Updated", "Supplier updated successfully!")
    show_suppliers()
    clear_fields()

def delete_supplier():
    selected = supplier_table.focus()
    if not selected:
        messagebox.showwarning("Select Supplier", "Please select a supplier to delete.")
        return
    supplier_id = supplier_table.item(selected)['values'][0]

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this supplier?")
    if confirm:
        cursor.execute("DELETE FROM suppliers WHERE id=?", (supplier_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Supplier deleted successfully!")
        show_suppliers()

tk.Button(frame_btn, text="Add Supplier", command=add_supplier, bg="#27AE60", fg="white",
          width=15).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="Update Supplier", command=update_supplier, bg="#2980B9", fg="white",
          width=15).grid(row=0, column=1, padx=10)
tk.Button(frame_btn, text="Delete Supplier", command=delete_supplier, bg="#E74C3C", fg="white",
          width=15).grid(row=0, column=2, padx=10)
tk.Button(frame_btn, text="Clear Fields", command=clear_fields, bg="#7F8C8D", fg="white",
          width=15).grid(row=0, column=3, padx=10)


frame_list = tk.LabelFrame(root, text="Suppliers List", bg="#EAF0F1", font=('Arial', 12, 'bold'))
frame_list.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Name", "Contact", "Email", "Address")
supplier_table = ttk.Treeview(frame_list, columns=columns, show="headings", height=8)
for col in columns:
    supplier_table.heading(col, text=col)
    supplier_table.column(col, width=150)
supplier_table.pack(fill="both", expand=True)

def show_suppliers():
    for row in supplier_table.get_children():
        supplier_table.delete(row)
    cursor.execute("SELECT * FROM suppliers")
    for supplier in cursor.fetchall():
        supplier_table.insert("", "end", values=supplier)

def on_supplier_select(event):
    selected = supplier_table.focus()
    if selected:
        values = supplier_table.item(selected, "values")
        name_var.set(values[1])
        contact_var.set(values[2])
        email_var.set(values[3])
        address_var.set(values[4])
        show_transactions(values[0])

supplier_table.bind("<ButtonRelease-1>", on_supplier_select)

frame_trans = tk.LabelFrame(root, text="Supplier Transactions", bg="#EAF0F1", font=('Arial', 12, 'bold'))
frame_trans.pack(fill="both", expand=True, padx=10, pady=5)

tk.Label(frame_trans, text="Item:", bg="#EAF0F1").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_trans, text="Amount:", bg="#EAF0F1").grid(row=0, column=2, padx=5, pady=5)

item_var = tk.StringVar()
amount_var = tk.StringVar()

tk.Entry(frame_trans, textvariable=item_var, width=25).grid(row=0, column=1, padx=5, pady=5)
tk.Entry(frame_trans, textvariable=amount_var, width=25).grid(row=0, column=3, padx=5, pady=5)

def add_transaction():
    selected = supplier_table.focus()
    if not selected:
        messagebox.showwarning("Select Supplier", "Please select a supplier first.")
        return
    supplier_id = supplier_table.item(selected)['values'][0]
    item = item_var.get()
    amount = amount_var.get()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if item == "" or amount == "":
        messagebox.showerror("Error", "Please fill all fields!")
        return

    cursor.execute("INSERT INTO supplier_transactions (supplier_id, item, amount, date) VALUES (?, ?, ?, ?)",
                   (supplier_id, item, amount, date))
    conn.commit()
    messagebox.showinfo("Success", "Transaction added successfully!")
    show_transactions(supplier_id)
    item_var.set("")
    amount_var.set("")

tk.Button(frame_trans, text="Add Transaction", command=add_transaction, bg="#16A085", fg="white", width=20).grid(row=0, column=4, padx=10)

columns_t = ("ID", "Item", "Amount", "Date")
transaction_table = ttk.Treeview(frame_trans, columns=columns_t, show="headings", height=6)
for col in columns_t:
    transaction_table.heading(col, text=col)
    transaction_table.column(col, width=150)
transaction_table.grid(row=1, column=0, columnspan=5, pady=10)

def show_transactions(supplier_id):
    for row in transaction_table.get_children():
        transaction_table.delete(row)
    cursor.execute("SELECT id, item, amount, date FROM supplier_transactions WHERE supplier_id=?", (supplier_id,))
    for trans in cursor.fetchall():
        transaction_table.insert("", "end", values=trans)

show_suppliers()

root.mainloop()
