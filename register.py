import tkinter as tk
from tkinter import messagebox
import os
from database import register_user

def register_window(login_window):
    register = tk.Toplevel(login_window)
    register.title("Create Account")
    register.geometry("500x700")
    register.resizable(False, False)

    # Keep registration window above login
    register.transient(login_window)
    register.grab_set()

    # COLORS
    background_color = "#F4F7FB"
    card_color = "#FFFFFF"
    primary_color = "#2563EB"
    text_color = "#1E293B"
    secondary_text = "#64748B"

    register.configure(
        bg=background_color)

    # IMAGE PATHS
    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )
    image_folder = os.path.join(
        base_dir,
        "images"
    )
    close_eye_path = os.path.join(
        image_folder,
        "closeeye.png"
    )
    open_eye_path = os.path.join(
        image_folder,
        "openeye.png"
    )
    close_eye_image = tk.PhotoImage(
        master=register,
        file=close_eye_path
    )
    open_eye_image = tk.PhotoImage(
        master=register,
        file=open_eye_path
    )
    # Keep references alive
    register.close_eye_image = close_eye_image
    register.open_eye_image = open_eye_image

    # MAIN CARD
    card = tk.Frame(
        register,
        bg=card_color,
        width=400,
        height=630
    )

    card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )
    card.pack_propagate(False)

    # TITLE
    title = tk.Label(
        card,
        text="Create Account",
        font=("Arial", 24, "bold"),
        fg=text_color,
        bg=card_color
    )
    title.pack(
        pady=(30, 5)
    )

    # SUBTITLE
    subtitle = tk.Label(
        card,
        text="Create your Expense Tracker account",
        font=("Arial", 10),
        fg=secondary_text,
        bg=card_color
    )
    subtitle.pack(
        pady=(0, 20)
    )

    # NAME
    tk.Label(
        card,
        text="Name",
        font=("Arial", 10, "bold"),
        fg=text_color,
        bg=card_color
    ).pack(
        anchor="w",
        padx=45,
        pady=(5, 4)
    )
    name_entry = tk.Entry(
        card,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )

    name_entry.pack(
        padx=45,
        fill="x",
        ipady=7
    )

    # USERNAME
    tk.Label(
        card,
        text="Username",
        font=("Arial", 10, "bold"),
        fg=text_color,
        bg=card_color
    ).pack(
        anchor="w",
        padx=45,
        pady=(12, 4)
    )
    username_entry = tk.Entry(
        card,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )
    username_entry.pack(
        padx=45,
        fill="x",
        ipady=7
    )

    # EMAIL
    tk.Label(
        card,
        text="Email",
        font=("Arial", 10, "bold"),
        fg=text_color,
        bg=card_color
    ).pack(
        anchor="w",
        padx=45,
        pady=(12, 4)
    )
    email_entry = tk.Entry(
        card,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )
    email_entry.pack(
        padx=45,
        fill="x",
        ipady=7
    )

    # PASSWORD LABEL
    tk.Label(
        card,
        text="Password",
        font=("Arial", 10, "bold"),
        fg=text_color,
        bg=card_color
    ).pack(
        anchor="w",
        padx=45,
        pady=(12, 4)
    )

    # PASSWORD FRAME
    password_frame = tk.Frame(
        card,
        bg=card_color,
        highlightbackground="#CBD5E1",
        highlightcolor=primary_color,
        highlightthickness=1
    )

    password_frame.pack(
        padx=45,
        fill="x"
    )

    # PASSWORD ENTRY
    password_entry = tk.Entry(
        password_frame,
        font=("Arial", 11),
        show="*",
        relief="flat",
        bd=0
    )

    password_entry.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        ipady=8
    )

    # PASSWORD VISIBILITY
    password_visible = False

    def toggle_password():
        nonlocal password_visible
        if password_visible:
            password_entry.config(
                show="*"
            )
            eye_button.config(
                image=close_eye_image
            )
            eye_button.image = close_eye_image
            password_visible = False

        else:
            password_entry.config(
                show="")
            eye_button.config(
                image=open_eye_image)
            eye_button.image = open_eye_image
            password_visible = True

    # EYE BUTTON
    eye_button = tk.Button(
        password_frame,
        image=close_eye_image,
        bg=card_color,
        activebackground=card_color,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=toggle_password
    )
    eye_button.pack(
        side="right",
        padx=8)

    # Keep image reference on button
    eye_button.image = close_eye_image

    # CREATE ACCOUNT FUNCTION
    def create_account():
        name = name_entry.get().strip()
        username = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()

        # VALIDATION
        if not name:
            messagebox.showerror(
                "Error",
                "Please enter your name.",
                parent=register
            )
            name_entry.focus_set()
            return

        if not username:
            messagebox.showerror(
                "Error",
                "Please enter a username.",
                parent=register
            )
            username_entry.focus_set()
            return

        if not email:
            messagebox.showerror(
                "Error",
                "Please enter your email.",
                parent=register
            )
            email_entry.focus_set()
            return

        if not password:
            messagebox.showerror(
                "Error",
                "Please enter your password.",
                parent=register
            )
            password_entry.focus_set()
            return

        # REGISTER USER
        try:
            register_user(
                name,
                username,
                email,
                password
            )
            messagebox.showinfo(
                "Success",
                "Account created successfully!",
                parent=register
            )

            # Close registration page
            register.grab_release()
            register.destroy()

            # Return focus to login
            login_window.deiconify()
            login_window.lift()
            login_window.focus_force()

        except Exception as e:
            error_message = str(e)
            if (
                "username" in error_message.lower()
                and "duplicate" in error_message.lower()):
                error_message = "Username already exists."
            elif (
                "email" in error_message.lower()
                and "duplicate" in error_message.lower()
            ):
                error_message = "Email already exists."
            messagebox.showerror(
                "Registration Error",
                error_message,
                parent=register
            )

    # CREATE ACCOUNT BUTTON
    register_button = tk.Button(
        card,
        text="Create Account",
        font=("Arial", 11, "bold"),
        bg=primary_color,
        fg="white",
        activebackground=primary_color,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        width=30,
        height=2,
        command=create_account
    )
    register_button.pack(
        pady=(22, 12)
    )
    
    # BACK TO LOGIN PAGE
    def back_to_login():

        register.grab_release()
        register.destroy()

        login_window.deiconify()
        login_window.lift()
        login_window.focus_force()

    back_button = tk.Button(
        card,
        text="Already have an account? Login",
        font=("Arial", 10),
        bg=card_color,
        fg=primary_color,
        activebackground=card_color,
        activeforeground=primary_color,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=back_to_login
    )

    back_button.pack()
    name_entry.focus_set()
