import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

conn = sqlite3.connect("al_habiba.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_name TEXT NOT NULL,
        quantity REAL NOT NULL,
        min_stock REAL NOT NULL
    )
""")
conn.commit()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()
    for row in rows:
        # Highlight low stock rows in red
        if row[2] <= row[3]:
            tree.insert("", tk.END, values=row, tags=("low_stock",))
        else:
            tree.insert("", tk.END, values=row)

    update_alert_label()

def add_material():
    name = name_entry.get().strip()
    qty = qty_entry.get().strip()
    min_qty = min_entry.get().strip()

    if not name or not qty or not min_qty:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    try:
        qty = float(qty)
        min_qty = float(min_qty)
        cursor.execute("INSERT INTO inventory (material_name, quantity, min_stock) VALUES (?, ?, ?)",
                       (name, qty, min_qty))
        conn.commit()
        refresh_table()
        clear_fields()
        messagebox.showinfo("Success", "Material added successfully!")
    except ValueError:
        messagebox.showerror("Invalid Input", "Quantity must be a number.")

def select_material(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        name_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)
        min_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        qty_entry.insert(0, values[2])
        min_entry.insert(0, values[3])

def update_material():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a material to update.")
        return
    values = tree.item(selected, "values")
    new_name = name_entry.get().strip()
    new_qty = qty_entry.get().strip()
    new_min = min_entry.get().strip()

    if not new_name or not new_qty or not new_min:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return
    try:
        cursor.execute("UPDATE inventory SET material_name=?, quantity=?, min_stock=? WHERE id=?",
                       (new_name, float(new_qty), float(new_min), values[0]))
        conn.commit()
        refresh_table()
        messagebox.showinfo("Success", "Material updated successfully!")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

def delete_material():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a material to delete.")
        return
    values = tree.item(selected, "values")
    confirm = messagebox.askyesno("Confirm Delete", f"Delete '{values[1]}'?")
    if confirm:
        cursor.execute("DELETE FROM inventory WHERE id=?", (values[0],))
        conn.commit()
        refresh_table()
        clear_fields()
        messagebox.showinfo("Deleted", "Material deleted successfully!")

def clear_fields():
    name_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    min_entry.delete(0, tk.END)

def update_alert_label():
    cursor.execute("SELECT COUNT(*) FROM inventory WHERE quantity <= min_stock")
    low_count = cursor.fetchone()[0]
    if low_count > 0:
        alert_label.config(text=f"⚠️ {low_count} item(s) below minimum stock!", fg="red")
    else:
        alert_label.config(text="✅ All stocks are sufficient.", fg="green")

root = tk.Tk()
root.title("Al-Habiba Restaurant - Inventory Management")
root.geometry("900x600")
root.config(bg="#ff8080")
label = tk.Label(root, text="Al-Habiba Restaurant", font=("Arial", 16, "bold"),
                 fg="#000099", bg="#00b3b3")
label.pack(pady=20)

form_frame = tk.Frame(root, bg="#FFE7A0")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Material Name:", font=("Arial", 12, "bold"), bg="#FFE7A0").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(form_frame, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Quantity:", font=("Arial", 12, "bold"), bg="#FFE7A0").grid(row=0, column=2, padx=5, pady=5)
qty_entry = tk.Entry(form_frame, font=("Arial", 12))
qty_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(form_frame, text="Min Stock:", font=("Arial", 12, "bold"), bg="#FFE7A0").grid(row=0, column=4, padx=5, pady=5)
min_entry = tk.Entry(form_frame, font=("Arial", 12))
min_entry.grid(row=0, column=5, padx=5, pady=5)

btn_frame = tk.Frame(root, bg="#FFE7A0")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", command=add_material, width=12, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=update_material, width=12, bg="#2196F3", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_material, width=12, bg="#F44336", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Refresh", command=refresh_table, width=12, bg="#FF9800", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=3, padx=5)

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("ID", "Material Name", "Quantity", "Min Stock")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
tree.heading("ID", text="ID")
tree.heading("Material Name", text="Material Name")
tree.heading("Quantity", text="Quantity")
tree.heading("Min Stock", text="Min Stock")

tree.column("ID", width=50, anchor=tk.CENTER)
tree.column("Material Name", width=250)
tree.column("Quantity", width=100, anchor=tk.CENTER)
tree.column("Min Stock", width=100, anchor=tk.CENTER)

tree.tag_configure("low_stock", background="#FFB6B6")  # Light red for low stock

tree.bind("<ButtonRelease-1>", select_material)
tree.pack(fill=tk.BOTH, expand=True)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4B3621", foreground="white")
style.configure("Treeview", font=("Arial", 11), background="#FFF8E7", foreground="black", rowheight=28)
style.map("Treeview", background=[("selected", "#FFD580")])

alert_label = tk.Label(root, text="", font=("Arial", 13, "bold"), bg="#FFE7A0")
alert_label.pack(pady=10)

refresh_table()

root.mainloop()
