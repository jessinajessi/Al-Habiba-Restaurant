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
    total_amount REAL,
    date TEXT
)
""")
conn.commit()

root = tk.Tk()
root.title("Al-Habiba Restaurant - Reports & Analytics")
root.geometry("1100x700")
root.configure(bg="#ff8080")

label = tk.Label(root, text="Al-Habiba Restaurant",
                 font=("Arial", 18, "bold"), fg="#000099", bg="#00b3b3", pady=10)
label.pack(fill="x")

summary_frame = tk.Frame(root, bg="#f7f7f7")
summary_frame.pack(pady=10, fill="x")

total_sales_label = tk.Label(summary_frame, text="Total Sales: ₹0.00", font=("Arial", 14, "bold"), bg="#f7f7f7")
total_sales_label.grid(row=0, column=0, padx=30, pady=5)

total_orders_label = tk.Label(summary_frame, text="Total Orders: 0", font=("Arial", 14, "bold"), bg="#f7f7f7")
total_orders_label.grid(row=0, column=1, padx=30, pady=5)

average_label = tk.Label(summary_frame, text="Average Bill: ₹0.00", font=("Arial", 14, "bold"), bg="#f7f7f7")
average_label.grid(row=0, column=2, padx=30, pady=5)

filter_frame = tk.LabelFrame(root, text="📅 Filter by Date Range", font=("Arial", 12, "bold"), bg="#f7f7f7")
filter_frame.pack(fill="x", padx=20, pady=10)

tk.Label(filter_frame, text="From (YYYY-MM-DD):", bg="#f7f7f7").grid(row=0, column=0, padx=10, pady=5)
start_date_entry = tk.Entry(filter_frame, width=15)
start_date_entry.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="To (YYYY-MM-DD):", bg="#f7f7f7").grid(row=0, column=2, padx=10, pady=5)
end_date_entry = tk.Entry(filter_frame, width=15)
end_date_entry.grid(row=0, column=3, padx=5)

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def load_filtered_sales():
    start = start_date_entry.get().strip()
    end = end_date_entry.get().strip()

    if not start or not end:
        messagebox.showwarning("Input Error", "Please enter both start and end dates.")
        return

    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")

        cursor.execute("""
            SELECT invoice_no, customer_name, total_amount, date
            FROM sales 
            WHERE date BETWEEN ? AND ? 
            ORDER BY date DESC
        """, (start, end))
        records = cursor.fetchall()

        update_sales_table(records)
        update_summary(records)

    except ValueError:
        messagebox.showerror("Invalid Date", "Dates must be in YYYY-MM-DD format.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

tk.Button(
    filter_frame,
    text="Show Report",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
    command=load_filtered_sales
).grid(row=0, column=4, padx=20)

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("Invoice No", "Customer Name", "Amount", "Date")
sales_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

for col in columns:
    sales_table.heading(col, text=col)
    sales_table.column(col, width=200, anchor="center")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=sales_table.yview)
sales_table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
sales_table.pack(fill="both", expand=True)

top_cust_frame = tk.LabelFrame(root, text="🏆 Top Customers", font=("Arial", 12, "bold"), bg="#f7f7f7")
top_cust_frame.pack(fill="x", padx=20, pady=10)

top_customers_list = tk.Listbox(top_cust_frame, font=("Arial", 12), height=5)
top_customers_list.pack(fill="x", padx=20, pady=10)

def update_summary(records=None):
    if records:
        total_sales = sum(safe_float(r[2]) for r in records)
        total_orders = len(records)
        avg = total_sales / total_orders if total_orders > 0 else 0
    else:
        cursor.execute("SELECT SUM(total_amount), COUNT(*), AVG(total_amount) FROM sales")
        result = cursor.fetchone() or (0, 0, 0)
        total_sales = safe_float(result[0])
        total_orders = int(result[1]) if result[1] else 0
        avg = safe_float(result[2])

    total_sales_label.config(text=f"Total Sales: ₹{total_sales:.2f}")
    total_orders_label.config(text=f"Total Orders: {total_orders}")
    average_label.config(text=f"Average Bill: ₹{avg:.2f}")

def update_sales_table(records=None):
    for item in sales_table.get_children():
        sales_table.delete(item)

    if records is None:
        cursor.execute("SELECT invoice_no, customer_name, total_amount, date FROM sales ORDER BY date DESC")
        records = cursor.fetchall()

    for row in records:
        invoice_no, customer, amount, date = row
        amount = safe_float(amount)
        sales_table.insert("", tk.END, values=(invoice_no, customer, f"₹{amount:.2f}", date))

def load_top_customers():
    cursor.execute("""
        SELECT customer_name, SUM(total_amount) as total_spent 
        FROM sales 
        WHERE total_amount IS NOT NULL
        GROUP BY customer_name 
        ORDER BY total_spent DESC 
        LIMIT 5
    """)
    top_customers = cursor.fetchall()

    top_customers_list.delete(0, tk.END)
    if not top_customers:
        top_customers_list.insert(tk.END, "No data available.")
    else:
        for cust in top_customers:
            name = cust[0] if cust[0] else "Unknown"
            total_spent = safe_float(cust[1])
            top_customers_list.insert(tk.END, f"{name} - ₹{total_spent:.2f}")

def refresh_data():
    update_sales_table()
    update_summary()
    load_top_customers()

refresh_btn = tk.Button(
    root,
    text="🔄 Refresh Data",
    bg="#2196F3",
    fg="white",
    font=("Arial", 12, "bold"),
    command=refresh_data
)
refresh_btn.pack(pady=10)

refresh_data()

root.mainloop()