import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

conn = sqlite3.connect("al_habiba.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier_name TEXT NOT NULL,
        item_name TEXT NOT NULL,
        quantity REAL NOT NULL,
        price REAL NOT NULL,
        total REAL NOT NULL,
        bill_no TEXT,
        purchase_date TEXT
    )
""")
conn.commit()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM purchases ORDER BY purchase_date DESC")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def clear_fields():
    supplier_entry.delete(0, tk.END)
    item_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    bill_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

def add_purchase():
    supplier = supplier_entry.get().strip()
    item = item_entry.get().strip()
    qty = qty_entry.get().strip()
    price = price_entry.get().strip()
    bill = bill_entry.get().strip()
    date = date_entry.get().strip()

    if not (supplier and item and qty and price):
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    try:
        qty = float(qty)
        price = float(price)
        total = qty * price
        # Auto date if empty
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO purchases (supplier_name, item_name, quantity, price, total, bill_no, purchase_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (supplier, item, qty, price, total, bill, date))
        conn.commit()
        refresh_table()
        clear_fields()
        messagebox.showinfo("Success", "Purchase record added successfully!")
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter valid numbers for Quantity and Price.")

def select_record(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        clear_fields()
        supplier_entry.insert(0, values[1])
        item_entry.insert(0, values[2])
        qty_entry.insert(0, values[3])
        price_entry.insert(0, values[4])
        bill_entry.insert(0, values[6])
        date_entry.insert(0, values[7])

def update_purchase():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to update.")
        return

    values = tree.item(selected, "values")
    supplier = supplier_entry.get().strip()
    item = item_entry.get().strip()
    qty = qty_entry.get().strip()
    price = price_entry.get().strip()
    bill = bill_entry.get().strip()
    date = date_entry.get().strip()

    if not (supplier and item and qty and price):
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    try:
        qty = float(qty)
        price = float(price)
        total = qty * price
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            UPDATE purchases
            SET supplier_name=?, item_name=?, quantity=?, price=?, total=?, bill_no=?, purchase_date=?
            WHERE id=?
        """, (supplier, item, qty, price, total, bill, date, values[0]))
        conn.commit()
        refresh_table()
        clear_fields()
        messagebox.showinfo("Success", "Purchase record updated successfully!")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")

def delete_purchase():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to delete.")
        return

    values = tree.item(selected, "values")
    confirm = messagebox.askyesno("Confirm Delete", f"Delete purchase record for '{values[1]}'?")
    if confirm:
        cursor.execute("DELETE FROM purchases WHERE id=?", (values[0],))
        conn.commit()
        refresh_table()
        clear_fields()
        messagebox.showinfo("Deleted", "Record deleted successfully!")

root = tk.Tk()
root.title("Al-Habiba Restaurant - Purchase Management")
root.geometry("950x620")
root.config(bg="#ff8080")
label = tk.Label(root, text="Al-Habiba Restaurant", font=("Arial", 16, "bold"),
                 fg="#000099", bg="#00b3b3")
label.pack(pady=20)
form_frame = tk.Frame(root, bg="#FFF8DC", pady=10)
form_frame.pack(pady=5)

tk.Label(form_frame, text="Supplier Name:", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=0, column=0, padx=5, pady=5)
supplier_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
supplier_entry.grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="Item Name:", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=0, column=2, padx=5)
item_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
item_entry.grid(row=0, column=3, padx=5)

tk.Label(form_frame, text="Quantity:", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=1, column=0, padx=5, pady=5)
qty_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
qty_entry.grid(row=1, column=1, padx=5)

tk.Label(form_frame, text="Price (₹):", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=1, column=2, padx=5)
price_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
price_entry.grid(row=1, column=3, padx=5)

tk.Label(form_frame, text="Bill No:", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=2, column=0, padx=5, pady=5)
bill_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
bill_entry.grid(row=2, column=1, padx=5)

tk.Label(form_frame, text="Date (Auto-filled):", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=2, column=2, padx=5)
date_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
date_entry.grid(row=2, column=3, padx=5)

btn_frame = tk.Frame(root, bg="#FFF8DC")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", command=add_purchase, width=12, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=update_purchase, width=12, bg="#2196F3", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_purchase, width=12, bg="#F44336", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Refresh", command=refresh_table, width=12, bg="#FF9800", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_fields, width=12, bg="#795548", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=4, padx=5)

tree_frame = tk.Frame(root, bg="#FFDAB9")
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("ID", "Supplier", "Item", "Qty", "Price", "Total", "Bill No", "Date")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=110)
tree.column("Supplier", width=150)
tree.column("Item", width=150)

tree.bind("<ButtonRelease-1>", select_record)
tree.pack(fill=tk.BOTH, expand=True)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                background="#8B4513", foreground="white")
style.configure("Treeview", font=("Arial", 11),
                background="#FFFDE7", foreground="black", rowheight=28)
style.map("Treeview", background=[("selected", "#FFD580")])

refresh_table()
root.mainloop()
