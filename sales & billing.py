import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

conn = sqlite3.connect("al_habiba.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_no TEXT,
    customer_name TEXT,
    item_name TEXT,
    quantity REAL,
    price REAL,
    total REAL,
    date TEXT
)
""")
conn.commit()

def generate_invoice_no():
    now = datetime.now()
    return "INV" + now.strftime("%Y%m%d%H%M%S")

def add_item():
    customer = customer_entry.get().strip()
    item = item_entry.get().strip()
    qty = qty_entry.get().strip()
    price = price_entry.get().strip()

    if not (customer and item and qty and price):
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    try:
        qty = float(qty)
        price = float(price)
        total = qty * price
        invoice_no = invoice_label.cget("text")
        date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO sales (invoice_no, customer_name, item_name, quantity, price, total, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (invoice_no, customer, item, qty, price, total, date))
        conn.commit()

        tree.insert("", tk.END, values=(customer, item, qty, price, total))
        update_total()
        clear_item_fields()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for quantity and price.")

def update_total():
    total_amount = 0
    for child in tree.get_children():
        total_amount += float(tree.item(child, "values")[4])
    gst = total_amount * 0.05  # 5% GST
    grand_total = total_amount + gst
    subtotal_var.set(f"{total_amount:.2f}")
    gst_var.set(f"{gst:.2f}")
    total_var.set(f"{grand_total:.2f}")

def clear_item_fields():
    item_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def clear_all():
    for row in tree.get_children():
        tree.delete(row)
    customer_entry.delete(0, tk.END)
    subtotal_var.set("")
    gst_var.set("")
    total_var.set("")
    invoice_label.config(text=generate_invoice_no())

def print_receipt():
    customer = customer_entry.get().strip()
    if not customer:
        messagebox.showwarning("Missing Info", "Enter customer name before printing.")
        return

    receipt_window = tk.Toplevel(root)
    receipt_window.title("Invoice Receipt")
    receipt_window.geometry("400x500")
    receipt_text = tk.Text(receipt_window, font=("Courier New", 10))
    receipt_text.pack(fill=tk.BOTH, expand=True)

    receipt_text.insert(tk.END, "      Al-Habiba Restaurant\n")
    receipt_text.insert(tk.END, "       Sales & Billing Invoice\n")
    receipt_text.insert(tk.END, "-" * 40 + "\n")
    receipt_text.insert(tk.END, f"Invoice No: {invoice_label.cget('text')}\n")
    receipt_text.insert(tk.END, f"Customer: {customer}\n")
    receipt_text.insert(tk.END, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    receipt_text.insert(tk.END, "-" * 40 + "\n")
    receipt_text.insert(tk.END, f"{'Item':15}{'Qty':>5}{'Price':>8}{'Total':>10}\n")
    receipt_text.insert(tk.END, "-" * 40 + "\n")

    for child in tree.get_children():
        values = tree.item(child, "values")
        receipt_text.insert(tk.END, f"{values[1]:15}{values[2]:>5}{values[3]:>8}{values[4]:>10}\n")

    receipt_text.insert(tk.END, "-" * 40 + "\n")
    receipt_text.insert(tk.END, f"{'Subtotal:':25}{subtotal_var.get():>10}\n")
    receipt_text.insert(tk.END, f"{'GST (5%):':25}{gst_var.get():>10}\n")
    receipt_text.insert(tk.END, f"{'Grand Total:':25}{total_var.get():>10}\n")
    receipt_text.insert(tk.END, "-" * 40 + "\n")
    receipt_text.insert(tk.END, "     Thank you! Visit Again!\n")

    receipt_text.config(state="disabled")

root = tk.Tk()
root.title("Al-Habiba Restaurant - Sales & Billing")
root.geometry("900x600")
root.config(bg="#ff8080")
label = tk.Label(root, text="Al-Habiba Restaurant", font=("Arial", 16, "bold"),
                 fg="#000099", bg="#00b3b3")
label.pack(pady=20)

invoice_frame = tk.Frame(root, bg="#FFE4C4")
invoice_frame.pack(pady=10)
tk.Label(invoice_frame, text="Invoice No:", font=("Arial", 12, "bold"), bg="#FFE4C4").pack(side=tk.LEFT)
invoice_label = tk.Label(invoice_frame, text=generate_invoice_no(), font=("Arial", 12, "bold"), bg="#FFE4C4", fg="blue")
invoice_label.pack(side=tk.LEFT, padx=5)

form_frame = tk.Frame(root, bg="#FFF8DC", pady=10)
form_frame.pack(pady=5)

tk.Label(form_frame, text="Customer Name:", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=0, column=0, padx=5, pady=5)
customer_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
customer_entry.grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="Item Name:", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=1, column=0, padx=5)
item_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
item_entry.grid(row=1, column=1, padx=5)

tk.Label(form_frame, text="Quantity:", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=1, column=2, padx=5)
qty_entry = tk.Entry(form_frame, font=("Arial", 12), width=10)
qty_entry.grid(row=1, column=3, padx=5)

tk.Label(form_frame, text="Price (₹):", font=("Arial", 12, "bold"), bg="#FFF8DC").grid(row=1, column=4, padx=5)
price_entry = tk.Entry(form_frame, font=("Arial", 12), width=10)
price_entry.grid(row=1, column=5, padx=5)

tk.Button(form_frame, text="Add Item", command=add_item, width=12, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).grid(row=1, column=6, padx=10)

tree_frame = tk.Frame(root, bg="#FFE4C4")
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("Customer", "Item", "Qty", "Price", "Total")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=150)
tree.pack(fill=tk.BOTH, expand=True)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#8B4513", foreground="white")
style.configure("Treeview", font=("Arial", 11), background="#FFFDE7", foreground="black", rowheight=28)
style.map("Treeview", background=[("selected", "#FFD580")])

total_frame = tk.Frame(root, bg="#FFE4C4", pady=10)
total_frame.pack(pady=10)

subtotal_var = tk.StringVar()
gst_var = tk.StringVar()
total_var = tk.StringVar()

tk.Label(total_frame, text="Subtotal (₹):", font=("Arial", 12, "bold"), bg="#FFE4C4").grid(row=0, column=0, padx=5)
tk.Entry(total_frame, textvariable=subtotal_var, font=("Arial", 12), width=12, state="readonly").grid(row=0, column=1, padx=5)
tk.Label(total_frame, text="GST (5%):", font=("Arial", 12, "bold"), bg="#FFE4C4").grid(row=0, column=2, padx=5)
tk.Entry(total_frame, textvariable=gst_var, font=("Arial", 12), width=12, state="readonly").grid(row=0, column=3, padx=5)
tk.Label(total_frame, text="Grand Total (₹):", font=("Arial", 12, "bold"), bg="#FFE4C4").grid(row=0, column=4, padx=5)
tk.Entry(total_frame, textvariable=total_var, font=("Arial", 12), width=12, state="readonly").grid(row=0, column=5, padx=5)

btn_frame = tk.Frame(root, bg="#FFE4C4")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="New Bill", command=clear_all, width=12, bg="#2196F3", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Print Receipt", command=print_receipt, width=15, bg="#795548", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Exit", command=root.destroy, width=12, bg="#F44336", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5)

root.mainloop()
