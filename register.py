import tkinter as tk
from tkinter import messagebox
from database import register_user

def register_window(login_window):
    register = tk.Toplevel(login_window)
    register.title("Create Account")
    register.geometry("500x500")

    title = tk.Label(
        register,
        text="Create Account",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=25)

    # Name
    tk.Label(
        register,
        text="Name:",
        font=("Arial", 12)
    ).pack(pady=5)

    name_entry = tk.Entry(
        register,
        width=30
    )
    name_entry.pack(pady=5)

    # Username
    tk.Label(
        register,
        text="Username:",
        font=("Arial", 12)
    ).pack(pady=5)

    username_entry = tk.Entry(
        register,
        width=30
    )
    username_entry.pack(pady=5)

    # Email
    tk.Label(
        register,
        text="Email:",
        font=("Arial", 12)
    ).pack(pady=5)

    email_entry = tk.Entry(
        register,
        width=30
    )
    email_entry.pack(pady=5)

    # Password
    tk.Label(
        register,
        text="Password:",
        font=("Arial", 12)
    ).pack(pady=5)

    password_entry = tk.Entry(
        register,
        width=30,
        show="*"
    )
    password_entry.pack(pady=5)

    def create_account():

        name = name_entry.get().strip()
        username = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()

        # Check Name
        if not name:
            messagebox.showerror(
                "Error",
                "Please enter your name."
            )
            return

        # Check Username
        if not username:
            messagebox.showerror(
                "Error",
                "Please enter a username."
            )
            return

        # Check Email
        if not email:
            messagebox.showerror(
                "Error",
                "Please enter your email."
            )
            return

        # Check Password
        if not password:
            messagebox.showerror(
                "Error",
                "Please enter your password."
            )
            return

        try:
            register_user(
                name,
                username,
                email,
                password
            )
            messagebox.showinfo(
                "Success",
                "Account created successfully!"
            )
            register.destroy()

        except Exception as e:
            messagebox.showerror(
                "Registration Error",
                str(e)
            )

    # Register button
    register_button = tk.Button(
        register,
        text="Register",
        width=20,
        command=create_account
    )
    register_button.pack(pady=25)

    # Back to Login
    back_button = tk.Button(
        register,
        text="Back to Login",
        width=20,
        command=register.destroy
    )
    back_button.pack(pady=5)