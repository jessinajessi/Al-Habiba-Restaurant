import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sqlite3
from datetime import datetime


DB_FILE = "al_habiba.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS app_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_name TEXT DEFAULT 'Al-Habiba Restaurant',
    address TEXT DEFAULT 'Annur, Coimbatore',
    phone TEXT DEFAULT '9876543210',
    gst_number TEXT DEFAULT 'GSTIN1234',
    theme TEXT DEFAULT 'Light'
)
""")
conn.commit()

root = tk.Tk()
root.title("Al-Habiba Restaurant - Settings & Backup")
root.geometry("700x500")
root.configure(bg="#ff8080")
label = tk.Label(root, text="Al-Habiba Restaurant",font=("Arial", 16, "bold"), fg="#000099", bg="#00b3b3")
label.pack(pady=20)

settings_frame = tk.LabelFrame(root, text="App Settings", font=("Arial", 12, "bold"), bg="#f8f9fa")
settings_frame.pack(fill="x", padx=20, pady=10)

tk.Label(settings_frame, text="Restaurant Name:", bg="#f8f9fa").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Label(settings_frame, text="Address:", bg="#f8f9fa").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Label(settings_frame, text="Phone:", bg="#f8f9fa").grid(row=2, column=0, padx=10, pady=5, sticky="e")
tk.Label(settings_frame, text="GST Number:", bg="#f8f9fa").grid(row=3, column=0, padx=10, pady=5, sticky="e")
tk.Label(settings_frame, text="Theme:", bg="#f8f9fa").grid(row=4, column=0, padx=10, pady=5, sticky="e")

name_entry = tk.Entry(settings_frame, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5)
address_entry = tk.Entry(settings_frame, width=40)
address_entry.grid(row=1, column=1, padx=10, pady=5)
phone_entry = tk.Entry(settings_frame, width=40)
phone_entry.grid(row=2, column=1, padx=10, pady=5)
gst_entry = tk.Entry(settings_frame, width=40)
gst_entry.grid(row=3, column=1, padx=10, pady=5)
theme_combo = ttk.Combobox(settings_frame, values=["Light", "Dark"], state="readonly", width=37)
theme_combo.grid(row=4, column=1, padx=10, pady=5)

def load_settings():
    cursor.execute("SELECT * FROM app_settings LIMIT 1")
    data = cursor.fetchone()
    if data:
        name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        gst_entry.delete(0, tk.END)
        name_entry.insert(0, data[1])
        address_entry.insert(0, data[2])
        phone_entry.insert(0, data[3])
        gst_entry.insert(0, data[4])
        theme_combo.set(data[5])
    else:
        cursor.execute("INSERT INTO app_settings DEFAULT VALUES")
        conn.commit()
        load_settings()

def save_settings():
    name = name_entry.get()
    addr = address_entry.get()
    phone = phone_entry.get()
    gst = gst_entry.get()
    theme = theme_combo.get()

    if not name or not phone:
        messagebox.showwarning("Validation", "Please fill in Restaurant Name and Phone.")
        return

    cursor.execute("DELETE FROM app_settings")
    cursor.execute("""
        INSERT INTO app_settings (restaurant_name, address, phone, gst_number, theme)
        VALUES (?, ?, ?, ?, ?)
    """, (name, addr, phone, gst, theme))
    conn.commit()
    messagebox.showinfo("Success", "Settings updated successfully!")

backup_frame = tk.LabelFrame(root, text="Data Backup & Restore", font=("Arial", 12, "bold"), bg="#f8f9fa")
backup_frame.pack(fill="x", padx=20, pady=10)

def backup_database():
    backup_dir = filedialog.askdirectory(title="Select Backup Folder")
    if not backup_dir:
        return

    backup_file = os.path.join(backup_dir, f"al_habiba_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
    try:
        shutil.copy(DB_FILE, backup_file)
        messagebox.showinfo("Backup Complete", f"Database backup saved at:\n{backup_file}")
    except Exception as e:
        messagebox.showerror("Backup Failed", str(e))

def restore_database():
    restore_path = filedialog.askopenfilename(title="Select Backup File", filetypes=[("SQLite DB", "*.db")])
    if not restore_path:
        return

    try:
        conn.close()
        shutil.copy(restore_path, DB_FILE)
        messagebox.showinfo("Restore Complete", "Database has been successfully restored!\nPlease restart the app.")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Restore Failed", str(e))

tk.Button(backup_frame, text="💾 Backup Data", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
          command=backup_database).grid(row=0, column=0, padx=20, pady=15)

tk.Button(backup_frame, text="♻️ Restore Data", bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
          command=restore_database).grid(row=0, column=1, padx=20, pady=15)

tk.Button(root, text="💾 Save Settings", bg="#673AB7", fg="white", font=("Arial", 12, "bold"),
          command=save_settings).pack(pady=15)

load_settings()
root.mainloop()
