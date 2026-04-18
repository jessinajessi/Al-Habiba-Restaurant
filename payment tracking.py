
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

conn = sqlite3.connect("al_habiba.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customer_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    amount REAL,
    payment_type TEXT,     -- Received / Pending
    date TEXT,
    remarks TEXT
)
""")
conn.commit()

root = tk.Tk()
root.title("Al-Habiba Restaurant - Payment Tracking")
root.geometry("900x600")
root.configure(bg="#ff8080")

label = tk.Label(root, text="Al-Habiba Restaurant",
                 font=("Arial", 16, "bold"), fg="#000099", bg="#00b3b3")
label.pack(pady=20)

frame_form = tk.LabelFrame(root, text="Customer Payment Details", padx=10, pady=10,
                           bg="#F9FAFB", font=('Arial', 12, 'bold'))
frame_form.pack(fill="x", padx=10, pady=5)

tk.Label(frame_form, text="Customer Name:", bg="#F9FAFB").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Amount:", bg="#F9FAFB").grid(row=0, column=2, padx=5, pady=5)
tk.Label(frame_form, text="Payment Type:", bg="#F9FAFB").grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Remarks:", bg="#F9FAFB").grid(row=1, column=2, padx=5, pady=5)

customer_name_var = tk.StringVar()
amount_var = tk.StringVar()
payment_type_var = tk.StringVar()
remarks_var = tk.StringVar()

tk.Entry(frame_form, textvariable=customer_name_var, width=25).grid(row=0, column=1, padx=5, pady=5)
tk.Entry(frame_form, textvariable=amount_var, width=25).grid(row=0, column=3, padx=5, pady=5)

payment_type_cb = ttk.Combobox(frame_form, textvariable=payment_type_var,
                               values=["Received", "Pending"], width=22, state="readonly")
payment_type_cb.grid(row=1, column=1, padx=5, pady=5)

tk.Entry(frame_form, textvariable=remarks_var, width=25).grid(row=1, column=3, padx=5, pady=5)

frame_btn = tk.Frame(root, bg="#F9FAFB")
frame_btn.pack(pady=5)

def clear_fields():
    customer_name_var.set("")
    amount_var.set("")
    payment_type_var.set("")
    remarks_var.set("")

def add_payment():
    name = customer_name_var.get()
    amount = amount_var.get()
    pay_type = payment_type_var.get()
    remarks = remarks_var.get()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not (name and amount and pay_type):
        messagebox.showerror("Error", "Customer Name, Amount, and Payment Type are required.")
        return

    cursor.execute("""
        INSERT INTO customer_payments (customer_name, amount, payment_type, date, remarks)
        VALUES (?, ?, ?, ?, ?)
    """, (name, amount, pay_type, date, remarks))
    conn.commit()
    messagebox.showinfo("Success", "Payment recorded successfully!")
    show_payments()
    clear_fields()

def update_payment():
    selected = payment_table.focus()
    if not selected:
        messagebox.showwarning("Select Record", "Please select a record to update.")
        return
    payment_id = payment_table.item(selected)['values'][0]

    cursor.execute("""
        UPDATE customer_payments
        SET customer_name=?, amount=?, payment_type=?, remarks=?
        WHERE id=?
    """, (customer_name_var.get(), amount_var.get(), payment_type_var.get(), remarks_var.get(), payment_id))
    conn.commit()
    messagebox.showinfo("Updated", "Payment record updated successfully!")
    show_payments()
    clear_fields()

def delete_payment():
    selected = payment_table.focus()
    if not selected:
        messagebox.showwarning("Select Record", "Please select a record to delete.")
        return
    payment_id = payment_table.item(selected)['values'][0]
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this payment record?")
    if confirm:
        cursor.execute("DELETE FROM customer_payments WHERE id=?", (payment_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Payment record deleted successfully!")
        show_payments()

tk.Button(frame_btn, text="Add Payment", command=add_payment, bg="#27AE60", fg="white", width=15).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="Update Payment", command=update_payment, bg="#2980B9", fg="white", width=15).grid(row=0, column=1, padx=10)
tk.Button(frame_btn, text="Delete Payment", command=delete_payment, bg="#E74C3C", fg="white", width=15).grid(row=0, column=2, padx=10)
tk.Button(frame_btn, text="Clear Fields", command=clear_fields, bg="#7F8C8D", fg="white", width=15).grid(row=0, column=3, padx=10)

frame_list = tk.LabelFrame(root, text="Customer Payment Records", bg="#F9FAFB", font=('Arial', 12, 'bold'))
frame_list.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Customer Name", "Amount", "Payment Type", "Date", "Remarks")
payment_table = ttk.Treeview(frame_list, columns=columns, show="headings", height=10)
for col in columns:
    payment_table.heading(col, text=col)
    payment_table.column(col, width=140)
payment_table.pack(fill="both", expand=True)

def tag_rows():
    for row in payment_table.get_children():
        values = payment_table.item(row)['values']
        if len(values) > 3:
            if values[3] == "Pending":
                payment_table.item(row, tags=("pending",))
            elif values[3] == "Received":
                payment_table.item(row, tags=("received",))
    payment_table.tag_configure("pending", background="#FADBD8")
    payment_table.tag_configure("received", background="#D5F5E3")

def show_payments():
    for row in payment_table.get_children():
        payment_table.delete(row)
    cursor.execute("SELECT * FROM customer_payments ORDER BY date DESC")
    for payment in cursor.fetchall():
        payment_table.insert("", "end", values=payment)
    tag_rows()

def on_payment_select(event):
    selected = payment_table.focus()
    if selected:
        values = payment_table.item(selected, "values")
        customer_name_var.set(values[1])
        amount_var.set(values[2])
        payment_type_var.set(values[3])
        remarks_var.set(values[5])

payment_table.bind("<ButtonRelease-1>", on_payment_select)

frame_search = tk.Frame(root, bg="#F9FAFB")
frame_search.pack(fill="x", padx=10, pady=5)

tk.Label(frame_search, text="Search by Customer Name:", bg="#F9FAFB").pack(side="left", padx=5)
search_var = tk.StringVar()

def search_payment():
    search_text = search_var.get()
    for row in payment_table.get_children():
        payment_table.delete(row)
    cursor.execute("SELECT * FROM customer_payments WHERE customer_name LIKE ?", ('%' + search_text + '%',))
    for payment in cursor.fetchall():
        payment_table.insert("", "end", values=payment)
    tag_rows()

tk.Entry(frame_search, textvariable=search_var, width=30).pack(side="left", padx=5)
tk.Button(frame_search, text="Search", command=search_payment, bg="#16A085", fg="white", width=12).pack(side="left", padx=5)
tk.Button(frame_search, text="Show All", command=show_payments, bg="#5D6D7E", fg="white", width=12).pack(side="left", padx=5)

show_payments()
root.mainloop()
