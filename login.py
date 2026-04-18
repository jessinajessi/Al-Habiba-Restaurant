import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage


def check_login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    conn = sqlite3.connect('al_habiba.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customer WHERE Username=? AND Password=?", (username, password))
    conn.commit()
    result = cursor.fetchone()
    conn.close()


    if result:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")


root = tk.Tk()
root.geometry('900x600')
root.title("Al-Habiba Restaurant -Login System")
label = tk.Label(root, text="Al-Habiba Restuarant", font=("Arial", 16, "bold"),
                 fg="#000099", bg="#00b3b3")
label.pack(pady=20)
root.configure(bg="#ff8080")
image_file = PhotoImage(file = 'al-habiba image.png')
image = tk.Label(root, image=image_file)
image.pack()

form_frame = tk.Frame(root)
form_frame.pack(padx=10, pady=10)

username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(root, text="Login", command=check_login, bg="#237E74")
login_button.pack(pady=5)

root.mainloop()