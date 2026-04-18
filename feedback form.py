import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv

conn = sqlite3.connect("al_habiba.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        rating INTEGER NOT NULL,
        message TEXT NOT NULL
    )
''')
conn.commit()

root = tk.Tk()
root.title("Al-Habiba Restaurant - Feedback Form")
root.geometry("900x600")
root.configure(bg="#ff8080")

label = tk.Label(root, text="Al-Habiba Restaurant",
                 font=("Arial", 16, "bold"), fg="#000099", bg="#00b3b3")
label.pack(pady=20)

def clear_form():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    rating_var.set("Select")
    feedback_text.delete("1.0", tk.END)

def save_feedback():
    name = name_entry.get()
    email = email_entry.get()
    rating = rating_var.get()
    feedback = feedback_text.get("1.0", tk.END).strip()

    if not name or not email or not feedback or rating == "Select":
        messagebox.showwarning("Input Error", "Please fill all fields before submitting.")
        return

    with open("al_habiba_feedback.csv", "a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, rating, feedback])

    cursor.execute("INSERT INTO feedback (name, email, rating, message) VALUES (?, ?, ?, ?)",
                   (name, email, rating, feedback))
    conn.commit()

    messagebox.showinfo("Thank You", "Your feedback has been submitted!")
    clear_form()

def export_to_csv():
    cursor.execute("SELECT * FROM feedback")
    rows = cursor.fetchall()
    with open("exported_feedback.csv", "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Rating", "Feedback"])
        writer.writerows(rows)
    messagebox.showinfo("Export Complete", "Feedback exported to exported_feedback.csv")

tk.Label(root, text="Name", bg="#b3e0ff").pack(padx=5, pady=5)
name_entry = tk.Entry(root, width=40)
name_entry.pack(padx=5, pady=5)

tk.Label(root, text="Email", bg="#b3e0ff").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack(pady=5)

tk.Label(root, text="Rating (1 - Poor to 5 - Excellent)", bg="#b3e0ff").pack()
rating_var = tk.StringVar()
rating_var.set("Select")
rating_options = ["1", "2", "3", "4", "5"]
tk.OptionMenu(root, rating_var, *rating_options).pack(pady=5)

tk.Label(root, text="Your Feedback", bg="#b3e0ff").pack()
feedback_text = tk.Text(root, width=40, height=5)
feedback_text.pack(pady=5)

tk.Button(root, text="Submit Feedback", command=save_feedback, bg="#ff3300",
          padx=10, pady=5).pack(pady=10)

tk.Button(root, text="Export to CSV", command=export_to_csv, bg="#00ffff",
          padx=10, pady=5).pack(pady=5)

root.mainloop()