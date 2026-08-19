import tkinter as tk
from tkinter import messagebox
import os
from database import login_user
from register import register_window
# COLORS
BG_COLOR = "#F4F7FB"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#2563EB"
TEXT_COLOR = "#1E293B"
SECONDARY_TEXT = "#64748B"
BORDER_COLOR = "#CBD5E1"

# IMAGE PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

open_eye_path = os.path.join(
    IMAGE_DIR,
    "openeye.png"
)

close_eye_path = os.path.join(
    IMAGE_DIR,
    "closeeye.png"
)

# LOGIN WINDOW
login_window = tk.Tk()

login_window.title("Expense Tracker - Login")
login_window.geometry("500x650")
login_window.configure(
    bg=BG_COLOR
)
login_window.resizable(
    False,
    False
)
# PASSWORD STATE
password_visible = False

# LOAD EYE IMAGES
open_eye_image = tk.PhotoImage(
    master=login_window,
    file=open_eye_path
)

close_eye_image = tk.PhotoImage(
    master=login_window,
    file=close_eye_path
)

# Keep image references alive
login_window.open_eye_image = open_eye_image
login_window.close_eye_image = close_eye_image


# OPEN REGISTER PAGE
def open_register():
    register_window(login_window)

# SHOW / HIDE PASSWORD
def toggle_password():

    global password_visible

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
            show=""
        )
        eye_button.config(
            image=open_eye_image
        )
        eye_button.image = open_eye_image
        password_visible = True

# RESET LOGIN FORM AFTER LOGOUT
def reset_login_form():

    global password_visible

    # Clear username/email
    login_entry.delete(
        0,
        tk.END
    )

    # Clear password
    password_entry.delete(
        0,
        tk.END
    )

    # Hide password
    password_entry.config(
        show="*"
    )
    # Reset eye icon
    eye_button.config(
        image=close_eye_image
    )
    eye_button.image = close_eye_image
    # Reset password state
    password_visible = False
    # Focus username/email
    login_entry.focus_set()


# LOGIN
def login():
    login_value = login_entry.get().strip()
    password = password_entry.get()

    # VALIDATION
    if not login_value:
        messagebox.showerror(
            "Error",
            "Please enter your username or email."
        )
        login_entry.focus_set()
        return
    if not password:
        messagebox.showerror(
            "Error",
            "Please enter your password."
        )
        password_entry.focus_set()
        return

    # DATABASE LOGIN
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
            
        user_id = user[0]
        name = user[1]
        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {name}!"
        )

        # HIDE LOGIN WINDOW
        login_window.withdraw()
        # OPEN EXPENSE TRACKER
        from app import start_app
        start_app(
            user_id,
            name,
            login_window
        )

    except Exception as e:
        # Make login visible if something goes wrong
        login_window.deiconify()
        login_window.lift()
        login_window.focus_force()
        messagebox.showerror(
            "Error",
            str(e)
        )

# MAIN CARD
card = tk.Frame(
    login_window,
    bg=CARD_COLOR,
    width=390,
    height=520
)
card.pack(
    pady=55
)
card.pack_propagate(False)

# TITLE
title = tk.Label(
    card,
    text="Welcome Back",
    font=("Arial", 24, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR
)
title.pack(
    pady=(40, 5)
)

# SUBTITLE
subtitle = tk.Label(
    card,
    text="Login to your Expense Tracker account",
    font=("Arial", 10),
    fg=SECONDARY_TEXT,
    bg=CARD_COLOR
)
subtitle.pack(
    pady=(0, 28)
)

# USERNAME / EMAIL LABEL
login_label = tk.Label(
    card,
    text="Username or Email",
    font=("Arial", 10, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR
)

login_label.pack(
    anchor="w",
    padx=50
)

# USERNAME / EMAIL ENTRY
login_entry = tk.Entry(
    card,
    font=("Arial", 11),
    bd=1,
    relief="solid"
)

login_entry.pack(
    padx=50,
    pady=(7, 20),
    ipady=9,
    fill="x"
)

# PASSWORD LABEL
password_label = tk.Label(
    card,
    text="Password",
    font=("Arial", 10, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR
)

password_label.pack(
    anchor="w",
    padx=50
)

# PASSWORD FRAME
password_frame = tk.Frame(
    card,
    bg=CARD_COLOR,
    height=38,
    highlightbackground=BORDER_COLOR,
    highlightcolor=PRIMARY_COLOR,
    highlightthickness=1
)
password_frame.pack(
    padx=50,
    pady=(7, 20),
    fill="x"
)
password_frame.pack_propagate(False)

# PASSWORD ENTRY
password_entry = tk.Entry(
    password_frame,
    font=("Arial", 11),
    show="*",
    bd=0,
    relief="flat"
)
password_entry.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(10, 0)
)

# EYE BUTTON
eye_button = tk.Button(
    password_frame,
    image=close_eye_image,
    command=toggle_password,
    bg=CARD_COLOR,
    activebackground=CARD_COLOR,
    bd=0,
    relief="flat",
    cursor="hand2"
)

eye_button.pack(
    side="right",
    padx=8
)
# Keep image reference
eye_button.image = close_eye_image

# LOGIN BUTTON
login_button = tk.Button(
    card,
    text="Login",
    font=("Arial", 11, "bold"),
    width=30,
    height=2,
    bg=PRIMARY_COLOR,
    fg="white",
    activebackground=PRIMARY_COLOR,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    command=login
)
login_button.pack(
    pady=(5, 15)
)

# CREATING ACCOUNT
register_button = tk.Button(
    card,
    text="Don't have an account? Create Account",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=PRIMARY_COLOR,
    activebackground=CARD_COLOR,
    activeforeground=PRIMARY_COLOR,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=open_register
)

register_button.pack()
login_entry.focus_set()
login_window.mainloop()
