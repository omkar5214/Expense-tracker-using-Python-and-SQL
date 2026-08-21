import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from database import (
    add_expense,
    get_categories,
    get_expenses,
    get_total_expense,
    get_category_totals,
    update_expense,
    delete_expense
)

BG_COLOR = "#F4F7FB"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"
TEXT_COLOR = "#1E293B"
SECONDARY_TEXT = "#64748B"
BORDER_COLOR = "#CBD5E1"
DANGER_COLOR = "#DC2626"
DANGER_HOVER = "#B91C1C"
# START APP
def start_app(user_id, name, login_window):
    window = tk.Toplevel(login_window)
    window.title("Expense Tracker")
    window.geometry("1000x700")
    window.configure(
        bg=BG_COLOR
    )
    window.resizable(
        False,
        False
    )
    window.user_id = user_id
    window.user_name = name

    # HEADER
    header = tk.Frame(
        window,
        bg=CARD_COLOR,
        height=85
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(False)

    # HAMBURGER BUTTON
    menu_button = tk.Button(
        header,
        text="☰",
        font=("Arial", 28, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        activebackground=CARD_COLOR,
        activeforeground=TEXT_COLOR,
        relief="flat",
        bd=0,
        cursor="hand2"
    )
    menu_button.place(
        x=25,
        y=17
    )

    # APPLICATION TITLE
    tk.Label(
        header,
        text="Expense Tracker",
        font=("Arial", 22, "bold"),
        fg=TEXT_COLOR,
        bg=CARD_COLOR
    ).place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    # WELCOME
    tk.Label(
        header,
        text=f"Welcome, {name}",
        font=("Arial", 10),
        fg=SECONDARY_TEXT,
        bg=CARD_COLOR
    ).place(
        relx=0.95,
        rely=0.5,
        anchor="e"
    )

    # MAIN AREA
    main_area = tk.Frame(
        window,
        bg=BG_COLOR
    )
    main_area.pack(
        fill="both",
        expand=True
    )

    # SIDEBAR
    sidebar = tk.Frame(
        main_area,
        bg=CARD_COLOR,
        width=210
    )
    sidebar.pack_propagate(False)
    sidebar_visible = False
    # CONTENT AREA
    content = tk.Frame(
        main_area,
        bg=BG_COLOR
    )
    content.pack(
        side="left",
        fill="both",
        expand=True
    )

    # CLEAR CONTENT
    def clear_content():
        for widget in content.winfo_children():
            widget.destroy()

    # PAGE HEADER
    def create_page_header(
        title,
        subtitle
    ):
        header_card = tk.Frame(
            content,
            bg=CARD_COLOR,
            height=150
        )

        header_card.pack(
            fill="x",
            padx=35,
            pady=(30, 20)
        )
        header_card.pack_propagate(False)
        tk.Label(
            header_card,
            text=title,
            font=("Arial", 28, "bold"),
            fg=TEXT_COLOR,
            bg=CARD_COLOR
        ).pack(
            pady=(35, 5)
        )
        tk.Label(
            header_card,
            text=subtitle,
            font=("Arial", 10),
            fg=SECONDARY_TEXT,
            bg=CARD_COLOR
        ).pack()

# TOGGLE SIDEBAR
    def toggle_sidebar():
        nonlocal sidebar_visible
        if sidebar_visible:
            sidebar.pack_forget()
            sidebar_visible = False
        else:
            sidebar.pack(
                side="left",
                fill="y",
                before=content
            )
            sidebar_visible = True
    menu_button.config(
        command=toggle_sidebar
    )

    # SIDEBAR BUTTON
    def sidebar_button(
        text,
        command,
        danger=False
    ):
        return tk.Button(
            sidebar,
            text=text,
            font=("Arial", 11),
            anchor="w",
            padx=25,
            bg=CARD_COLOR,
            fg=(
                DANGER_COLOR
                if danger
                else TEXT_COLOR
            ),
            activebackground=BG_COLOR,
            activeforeground=(
                DANGER_HOVER
                if danger
                else PRIMARY_COLOR
            ),
            relief="flat",
            bd=0,
            cursor="hand2",
            command=command
        )

    # ADD EXPENSE
    def add_expense_window():
        expense_window = tk.Toplevel(
            window
        )
        expense_window.title(
            "Add Expense"
        )
        expense_window.geometry(
            "500x600"
        )
        expense_window.configure(
            bg=BG_COLOR
        )
        expense_window.resizable(
            False,
            False
        )

        # CARD
        card = tk.Frame(
            expense_window,
            bg=CARD_COLOR,
            width=420,
            height=530
        )
        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )
        card.pack_propagate(False)

        # TITLE
        tk.Label(
            card,
            text="Add Expense",
            font=("Arial", 22, "bold"),
            fg=TEXT_COLOR,
            bg=CARD_COLOR
        ).pack(
            pady=(25, 5)
        )

        tk.Label(
            card,
            text="Add a new expense to your account",
            font=("Arial", 10),
            fg=SECONDARY_TEXT,
            bg=CARD_COLOR
        ).pack(
            pady=(0, 20)
        )

        # AMOUNT
        tk.Label(
            card,
            text="Amount",
            font=("Arial", 10, "bold"),
            fg=TEXT_COLOR,
            bg=CARD_COLOR
        ).pack(
            anchor="w",
            padx=45,
            pady=(5, 4)
        )
        amount_entry = tk.Entry(
            card,
            font=("Arial", 11),
            bd=1,
            relief="solid"
        )

        amount_entry.pack(
            padx=45,
            fill="x",
            ipady=7
        )

        # CATEGORY
        tk.Label(
            card,
            text="Category",
            font=("Arial", 10, "bold"),
            fg=TEXT_COLOR,
            bg=CARD_COLOR
        ).pack(
            anchor="w",
            padx=45,
            pady=(12, 4)
        )

        categories = get_categories()
        category_box = ttk.Combobox(
            card,
            values=[
                category[1]
                for category in categories
            ],
            state="readonly"
        )

        category_box.pack(
            padx=45,
            fill="x",
            ipady=5
        )

        # DESCRIPTION
        tk.Label(
            card,
            text="Description",
            font=("Arial", 10, "bold"),
            fg=TEXT_COLOR,
            bg=CARD_COLOR
        ).pack(
            anchor="w",
            padx=45,
            pady=(12, 4)
        )
        description_entry = tk.Entry(
            card,
            font=("Arial", 11),
            bd=1,
            relief="solid"
        )
        description_entry.pack(
            padx=45,
            fill="x",
            ipady=7
        )

        # DATE
        tk.Label(
            card,
            text="Date",
            font=("Arial", 10, "bold"),
            fg=TEXT_COLOR,
            bg=CARD_COLOR
        ).pack(
            anchor="w",
            padx=45,
            pady=(12, 4)
        )
        date_entry = DateEntry(
            card,
            date_pattern="yyyy-mm-dd"
        )

        date_entry.pack(
            padx=45,
            fill="x",
            ipady=5
        )

        # SAVE
        def save_expense():
            try:
                amount_text = (
                    amount_entry
                    .get()
                    .strip()
                )
                category = (
                    category_box
                    .get()
                    .strip()
                )
                description = (
                    description_entry
                    .get()
                    .strip()
                )
                expense_date = (
                    date_entry
                    .get()
                    .strip()
                )

                if not amount_text:
                    messagebox.showerror(
                        "Error",
                        "Please enter an amount.",
                        parent=expense_window
                    )
                    amount_entry.focus_set()
                    return

                try:
                    amount = float(
                        amount_text
                    )
                except ValueError:
                    messagebox.showerror(
                        "Error",
                        "Amount must be a number.",
                        parent=expense_window
                    )
                    amount_entry.focus_set()
                    return

                if amount <= 0:
                    messagebox.showerror(
                        "Error",
                        "Amount must be greater than 0.",
                        parent=expense_window
                    )
                    return
                
                if not category:
                    messagebox.showerror(
                        "Error",
                        "Please select a category.",
                        parent=expense_window
                    )
                    return
            
                try:
                    datetime.strptime(
                        expense_date,
                        "%Y-%m-%d"
                    )

                except ValueError:
                    messagebox.showerror(
                        "Error",
                        "Invalid date.",
                        parent=expense_window
                    )
                    return

                # Find category ID
                category_id = None
                for category_data in categories:
                    if category_data[1] == category:
                        category_id = category_data[0]
                        break

                if category_id is None:
                    messagebox.showerror(
                        "Error",
                        "Invalid category.",
                        parent=expense_window
                    )
                    return

                # Insert expense
                add_expense(
                    user_id,
                    category_id,
                    amount,
                    description,
                    expense_date
                )
                messagebox.showinfo(
                    "Success",
                    "Expense added successfully!",
                    parent=expense_window
                )
                expense_window.destroy()

                # Refresh current page
                show_manage_expense()
            except Exception as e:
                messagebox.showerror(
                    "Database Error",
                    str(e),
                    parent=expense_window
                )

        tk.Button(
            card,
            text="Add Expense",
            font=("Arial", 11, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=PRIMARY_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            width=30,
            height=2,
            command=save_expense
        ).pack(
            pady=22
        )
        amount_entry.focus_set()

    # MANAGE EXPENSE
    def show_manage_expense():
        clear_content()
        create_page_header(
            "Manage Expense",
            "Add, update and delete your expenses"
        )

        # TABLE CARD
        table_card = tk.Frame(
            content,
            bg=CARD_COLOR
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 15)
        )
        columns = (
            "ID",
            "Description",
            "Date",
            "Category",
            "Amount"
        )
        table = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings"
        )
        for column in columns:
            table.heading(
                column,
                text=column
            )
        table.column(
            "ID",
            width=60,
            anchor="center"
        )
        table.column(
            "Description",
            width=300
        )

        table.column(
            "Date",
            width=140,
            anchor="center"
        )

        table.column(
            "Category",
            width=180,
            anchor="center"
        )
        table.column(
            "Amount",
            width=130,
            anchor="center"
        )
        expenses = get_expenses(
            user_id
        )
        for expense in expenses:
            table.insert(
                "",
                tk.END,
                values=(
                    expense[0],
                    expense[2],
                    expense[3],
                    expense[4],
                    f"₹{expense[1]:.2f}"
                )
            )
        table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # BUTTONS
        button_frame = tk.Frame(
            content,
            bg=BG_COLOR
        )
        button_frame.pack(
            pady=(0, 25)
        )

        # UPDATE
        def update_selected():
            selected = table.selection()
            if not selected:
                messagebox.showwarning(
                    "Warning",
                    "Please select an expense.",
                    parent=window
                )
                return
            
            values = table.item(
                selected[0],
                "values"
            )
            expense_id = values[0]
            update_window = tk.Toplevel(
                window
            )

            update_window.title(
                "Update Expense"
            )
            update_window.geometry(
                "450x350"
            )

            update_window.configure(
                bg=BG_COLOR
            )
            update_window.resizable(
                False,
                False
            )
            card = tk.Frame(
                update_window,
                bg=CARD_COLOR,
                width=380,
                height=300
            )
            card.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

            card.pack_propagate(False)
            tk.Label(
                card,
                text="Update Expense",
                font=("Arial", 20, "bold"),
                fg=TEXT_COLOR,
                bg=CARD_COLOR
            ).pack(
                pady=(20, 15)
            )
            # Amount
            tk.Label(
                card,
                text="Amount",
                font=("Arial", 10, "bold"),
                fg=TEXT_COLOR,
                bg=CARD_COLOR
            ).pack(
                anchor="w",
                padx=40,
                pady=(0, 4)
            )
            amount_entry = tk.Entry(
                card,
                font=("Arial", 11),
                bd=1,
                relief="solid"
            )
            amount_entry.pack(
                padx=40,
                fill="x",
                ipady=7
            )
            amount_entry.insert(
                0,
                values[4].replace(
                    "₹",
                    ""
                )
            )

            # Description
            tk.Label(
                card,
                text="Description",
                font=("Arial", 10, "bold"),
                fg=TEXT_COLOR,
                bg=CARD_COLOR
            ).pack(
                anchor="w",
                padx=40,
                pady=(12, 4)
            )
            description_entry = tk.Entry(
                card,
                font=("Arial", 11),
                bd=1,
                relief="solid"
            )

            description_entry.pack(
                padx=40,
                fill="x",
                ipady=7
            )
            description_entry.insert(
                0,
                values[1]
            )

            def save_update():
                try:
                    amount_text = (
                        amount_entry
                        .get()
                        .strip()
                    )
                    description = (
                        description_entry
                        .get()
                        .strip()
                    )

                    if not amount_text:
                        messagebox.showerror(
                            "Error",
                            "Please enter an amount.",
                            parent=update_window
                        )
                        return
                    
                    try:
                        amount = float(
                            amount_text
                        )
                    except ValueError:
                        messagebox.showerror(
                            "Error",
                            "Amount must be a number.",
                            parent=update_window
                        )
                        return
                    
                    if amount <= 0:
                        messagebox.showerror(
                            "Error",
                            "Amount must be greater than 0.",
                            parent=update_window
                        )
                        return
                    
                    update_expense(
                        expense_id,
                        amount,
                        description
                    )
                    messagebox.showinfo(
                        "Success",
                        "Expense updated successfully!",
                        parent=update_window
                    )
                    update_window.destroy()
                    show_manage_expense()
                except Exception as e:
                    messagebox.showerror(
                        "Database Error",
                        str(e),
                        parent=update_window
                    )
            tk.Button(
                card,
                text="Save Changes",
                font=("Arial", 11, "bold"),
                bg=PRIMARY_COLOR,
                fg="white",
                activebackground=PRIMARY_HOVER,
                activeforeground="white",
                relief="flat",
                bd=0,
                cursor="hand2",
                width=25,
                height=2,
                command=save_update
            ).pack(
                pady=20
            )

        # DELETE
        def delete_selected():
            selected = table.selection()
            if not selected:
                messagebox.showwarning(
                    "Warning",
                    "Please select an expense.",
                    parent=window
                )

                return
            values = table.item(
                selected[0],
                "values"
            )
            expense_id = values[0]
            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this expense?",
                parent=window
            )
            if not confirm:
                return
            try:
                delete_expense(
                    expense_id
                )
                messagebox.showinfo(
                    "Success",
                    "Expense deleted successfully!",
                    parent=window
                )
                show_manage_expense()
            except Exception as e:
                messagebox.showerror(
                    "Database Error",
                    str(e),
                    parent=window
                )

        # ADD BUTTON
        tk.Button(
            button_frame,
            text="Add Expense",
            font=("Arial", 10, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=PRIMARY_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            width=18,
            height=2,
            command=add_expense_window
        ).pack(
            side="left",
            padx=8
        )

        # UPDATE BUTTON
        tk.Button(
            button_frame,
            text="Update Selected",
            font=("Arial", 10, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=PRIMARY_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            width=18,
            height=2,
            command=update_selected
        ).pack(
            side="left",
            padx=8
        )

        # DELETE BUTTON
        tk.Button(
            button_frame,
            text="Delete Selected",
            font=("Arial", 10, "bold"),
            bg=DANGER_COLOR,
            fg="white",
            activebackground=DANGER_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            width=18,
            height=2,
            command=delete_selected
        ).pack(
            side="left",
            padx=8
        )

    # VIEW EXPENSE
    def show_view_expense():
        clear_content()
        create_page_header(
            "View Expense",
            "View all your recorded expenses"
        )

        # TABLE CARD
        table_card = tk.Frame(
            content,
            bg=CARD_COLOR
        )
        table_card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 15)
        )
        columns = (
            "Description",
            "Date",
            "Category",
            "Amount"
        )
        table = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings"
        )
        table.heading(
            "Description",
            text="Description"
        )
        table.heading(
            "Date",
            text="Date"
        )
        table.heading(
            "Category",
            text="Category"
        )
        table.heading(
            "Amount",
            text="Amount"
        )
        table.column(
            "Description",
            width=380
        )
        table.column(
            "Date",
            width=150,
            anchor="center"
        )
        table.column(
            "Category",
            width=180,
            anchor="center"
        )

        table.column(
            "Amount",
            width=150,
            anchor="center"
        )
        expenses = get_expenses(
            user_id
        )
        for expense in expenses:
            table.insert(
                "",
                tk.END,
                values=(
                    expense[2],
                    expense[3],
                    expense[4],
                    f"₹{expense[1]:.2f}"
                )
            )
        table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # TOTAL EXPENSE
        total_card = tk.Frame(
            content,
            bg=CARD_COLOR,
            height=80
        )
        total_card.pack(
            fill="x",
            padx=35,
            pady=(0, 25)
        )

        total_card.pack_propagate(False)
        total = get_total_expense(
            user_id
        )
        tk.Label(
            total_card,
            text="Total Expense",
            font=("Arial", 14, "bold"),
            fg=TEXT_COLOR,
            bg=CARD_COLOR
        ).pack(
            side="left",
            padx=25
        )
        tk.Label(
            total_card,
            text=f"₹{float(total):.2f}",
            font=("Arial", 20, "bold"),
            fg=PRIMARY_COLOR,
            bg=CARD_COLOR
        ).pack(
            side="right",
            padx=25
        )

    def show_summary():
        clear_content()
        create_page_header(
            "Summary",
            "Understand where your money is going"
        )
        summary_card = tk.Frame(
            content,
            bg=CARD_COLOR
        )
        summary_card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 30)
        )
        results = get_category_totals(
            user_id
        )

        if not results:
            tk.Label(
                summary_card,
                text="No expenses found.",
                font=("Arial", 14),
                fg=SECONDARY_TEXT,
                bg=CARD_COLOR
            ).pack(
                pady=50
            )
            return

        # TABLE
        columns = (
            "Category",
            "Total"
        )
        summary_table = ttk.Treeview(
            summary_card,
            columns=columns,
            show="headings"
        )
        summary_table.heading(
            "Category",
            text="Category"
        )
        summary_table.heading(
            "Total",
            text="Total Expense"
        )
        summary_table.column(
            "Category",
            width=400
        )
        summary_table.column(
            "Total",
            width=250,
            anchor="center"
        )

        for category, total in results:
            summary_table.insert("",tk.END,values=(category,f"₹{float(total):.2f}"))
        summary_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    # LOGOUT
    def logout():
        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=window
        )
        if not confirm:
            return
        window.destroy()


        # Reset login page
        from login import reset_login_form
        reset_login_form()
        login_window.deiconify()
        login_window.lift()
        login_window.focus_force()

    # SIDEBAR CONTENT
    tk.Label(
        sidebar,
        text="Menu",
        font=("Arial", 20, "bold"),
        fg=TEXT_COLOR,
        bg=CARD_COLOR
    ).pack(
        anchor="w",
        padx=25,
        pady=(30, 25)
    )
    sidebar_button(
        "Manage Expense",
        show_manage_expense
    ).pack(
        fill="x",
        pady=5
    )
    sidebar_button(
        "View Expense",
        show_view_expense
    ).pack(
        fill="x",
        pady=5
    )
    sidebar_button(
        "Summary",
        show_summary
    ).pack(
        fill="x",
        pady=5
    )

    # Separator
    tk.Frame(
        sidebar,
        bg=BORDER_COLOR,
        height=1
    ).pack(
        fill="x",
        padx=25,
        pady=25
    )

    sidebar_button(
        "Logout",
        logout,
        danger=True
    ).pack(
        fill="x",
        pady=5
    )

    # CLOSE APP
    def close_app():
        window.destroy()
        login_window.destroy()

    window.protocol(
        "WM_DELETE_WINDOW",
        close_app
    )

    show_view_expense()
