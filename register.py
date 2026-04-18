import sqlite3
import tkinter as tk
from tkinter import messagebox, PhotoImage

def register():
    name_val = name_entry.get()
    username_val = username_entry.get()
    mobile_val = mobile_entry.get()
    email_val = email_entry.get()
    password_val = password_entry.get()

    if username_val and password_val:
        conn = sqlite3.connect('al_habiba.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO customer
                    (Name, Username, Mobile, Email, Password) 
                    VALUES (?, ?, ?, ?, ?)""",
                       (name_val, username_val, mobile_val, email_val, password_val))
        conn.commit()


        messagebox.showinfo("Success", f"User {username_val} registered successfully!")
    else:
        messagebox.showerror("Error", "mobile and password are required.")


def login():
    root.destroy()
    import login


root = tk.Tk()
root.geometry('900x600')
root.title("Al-Habiba Restaurant - Registration Form")
root.configure(bg="#ff8080")

label = tk.Label(root, text="Al-Habiba Restaurant", font=("Arial", 16, "bold"),
                 fg="#000099", bg="#00b3b3")
label.pack(pady=20)
image_file = PhotoImage(file = 'al-habiba image.png')
image = tk.Label(root, image=image_file)
image.pack()

conn = sqlite3.connect('al_habiba.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Username TEXT UNIQUE,
        Mobile TEXT,
        Email TEXT UNIQUE,
        Password TEXT
    )
""")
conn.commit()
conn.close()

name_label = tk.Label(root, text="Name:")
name_label.pack(padx=2, pady=2)
name_entry = tk.Entry(root)
name_entry.pack(padx=2, pady=2)

username_label = tk.Label(root, text="Username:")
username_label.pack(padx=2, pady=2)
username_entry = tk.Entry(root)
username_entry.pack(padx=2, pady=2)

mobile_label = tk.Label(root, text="Mobile:")
mobile_label.pack(padx=2, pady=2)
mobile_entry = tk.Entry(root)
mobile_entry.pack(padx=2, pady=2)

email_label = tk.Label(root, text="Email:")
email_label.pack(padx=2, pady=2)
email_entry = tk.Entry(root)
email_entry.pack(padx=2, pady=2)

password_label = tk.Label(root, text="Password:")
password_label.pack(padx=2, pady=2)
password_entry = tk.Entry(root, show="*")
password_entry.pack(padx=2, pady=2)

register_button = tk.Button(root, text="Register", command=register, bg="#237E74", fg="white")
register_button.pack(pady=5)

login_button = tk.Button(root, text="Login", command=login, bg="#237E74", fg="white")
login_button.pack(pady=5)

root.mainloop()
