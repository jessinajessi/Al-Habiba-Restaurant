import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

conn = sqlite3.connect("al_habiba.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        price REAL NOT NULL
    )
""")
conn.commit()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM menu")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def add_item():
    name = name_entry.get().strip()
    price = price_entry.get().strip()
    if not name or not price:
        messagebox.showwarning("Input Error", "Please enter item name and price.")
        return
    try:
        cursor.execute("INSERT INTO menu (item_name, price) VALUES (?, ?)", (name, float(price)))
        conn.commit()
        refresh_table()
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Item added successfully!")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid price.")

def select_item(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        price_entry.insert(0, values[2])

def update_item():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an item to update.")
        return
    values = tree.item(selected, "values")
    new_name = name_entry.get().strip()
    new_price = price_entry.get().strip()
    if not new_name or not new_price:
        messagebox.showwarning("Input Error", "Please enter both name and price.")
        return
    try:
        cursor.execute("UPDATE menu SET item_name=?, price=? WHERE id=?", (new_name, float(new_price), values[0]))
        conn.commit()
        refresh_table()
        messagebox.showinfo("Success", "Item updated successfully!")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid price.")

def delete_item():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an item to delete.")
        return
    values = tree.item(selected, "values")
    confirm = messagebox.askyesno("Confirm Delete", f"Delete '{values[1]}'?")
    if confirm:
        cursor.execute("DELETE FROM menu WHERE id=?", (values[0],))
        conn.commit()
        refresh_table()
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        messagebox.showinfo("Deleted", "Item deleted successfully!")

root = tk.Tk()
root.title("Al-Habiba Restaurant - Menu Management")
root.geometry("900x600")
root.config(bg="#ff8080")
label = tk.Label(root, text="Al-Habiba Restaurant", font=("Arial", 16, "bold"),
                 fg="#000099", bg="#00b3b3")
label.pack(pady=20)

form_frame = tk.Frame(root, bg="#FFD580")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Item Name:", font=("Arial", 12, "bold"), bg="#FFD580").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(form_frame, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Price (₹):", font=("Arial", 12, "bold"), bg="#FFD580").grid(row=0, column=2, padx=5, pady=5)
price_entry = tk.Entry(form_frame, font=("Arial", 12))
price_entry.grid(row=0, column=3, padx=5, pady=5)

button_frame = tk.Frame(root, bg="#FFD580")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Item", command=add_item, width=12, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Item", command=update_item, width=12, bg="#2196F3", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Item", command=delete_item, width=12, bg="#F44336", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Refresh", command=refresh_table, width=12, bg="#FF9800", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=3, padx=5)

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("ID", "Item Name", "Price")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
tree.heading("ID", text="ID")
tree.heading("Item Name", text="Item Name")
tree.heading("Price", text="Price (₹)")
tree.column("ID", width=50, anchor=tk.CENTER)
tree.column("Item Name", width=300)
tree.column("Price", width=100, anchor=tk.CENTER)
tree.bind("<ButtonRelease-1>", select_item)
tree.pack(fill=tk.BOTH, expand=True)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"),bg="#4B3621",  fg="white")
style.configure("Treeview",font=("Arial", 11),bg="#FFF8E7", fg="black", rowheight=28,fieldbackground="#FFF8E7")

style.map("Treeview", bg=[("selected", "#FFB347")], fg=[("selected", "black")])

refresh_table()

root.mainloop()
