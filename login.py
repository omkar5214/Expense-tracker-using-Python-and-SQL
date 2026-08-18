import tkinter as tk
from tkinter import messagebox
from database import login_user
from register import register_window
from app import start_app

def open_register():
    register_window(login_window)

def login():
    login_value = login_entry.get().strip()
    password = password_entry.get()
    if not login_value:
        messagebox.showerror(
            "Error",
            "Please enter your username or email."
        )
        return

    if not password:
        messagebox.showerror(
            "Error",
            "Please enter your password."
        )
        return

    try:
        user = login_user(
            login_value,
            password
        )

        if user is None:
            messagebox.showerror(
                "Login Failed",
                "Invalid username/email or password."
            )
            return

        # returns to database.py:
        user_id = user[0]
        name = user[1]
        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {name}!"
        )
        # Hide login window
        login_window.withdraw()

        # Open Expense Tracker
        start_app(
            user_id,
            name
        )
        # Destroy login window after Expense Tracker closes
        login_window.destroy()

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )

# LOGIN WINDOW
login_window = tk.Tk()
login_window.title("Expense Tracker - Login")
login_window.geometry("500x450")

# TITLE
title = tk.Label(
    login_window,
    text="Expense Tracker",
    font=("Arial", 24, "bold")
)
title.pack(pady=40)

# USERNAME / EMAIL
tk.Label(
    login_window,
    text="Username or Email:",
    font=("Arial", 12)
).pack(pady=5)


login_entry = tk.Entry(
    login_window,
    width=30
)
login_entry.pack(pady=5)

# PASSWORD
tk.Label(
    login_window,
    text="Password:",
    font=("Arial", 12)
).pack(pady=5)


password_entry = tk.Entry(
    login_window,
    width=30,
    show="*"
)
password_entry.pack(pady=5)

# LOGIN BUTTON
login_button = tk.Button(
    login_window,
    text="Login",
    width=20,
    height=2,
    command=login
)
login_button.pack(pady=25)

# CREATE ACCOUNT BUTTON
register_button = tk.Button(
    login_window,
    text="Create New Account",
    width=20,
    command=open_register
)
register_button.pack(pady=5)

# START LOGIN
login_window.mainloop()