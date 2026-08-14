import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import (
    add_expense,
    get_categories,
    get_expenses,
    get_total_expense,
    get_category_totals
)
window = tk.Tk()
window.title("Expense Tracker")
window.geometry("800x600")


def add_expense_window():
    expense_window = tk.Toplevel(window)
    expense_window.title("Add Expense")
    expense_window.geometry("500x500")

    title = tk.Label(
        expense_window,
        text="Add Expense",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=25)

    # Amount
    tk.Label(
        expense_window,
        text="Amount:",
        font=("Arial", 12)
    ).pack(pady=5)

    amount_entry = tk.Entry(
        expense_window,
        width=30
    )
    amount_entry.pack(pady=5)

    # Category
    tk.Label(
        expense_window,
        text="Category:",
        font=("Arial", 12)
    ).pack(pady=5)

    categories = get_categories()

    category_box = ttk.Combobox(
        expense_window,
        values=[category[1] for category in categories],
        state="readonly",
        width=27
    )
    category_box.pack(pady=5)

    # Description
    tk.Label(
        expense_window,
        text="Description:",
        font=("Arial", 12)
    ).pack(pady=5)

    description_entry = tk.Entry(
        expense_window,
        width=30
    )
    description_entry.pack(pady=5)

    # Date
    tk.Label(
        expense_window,
        text="Date (YYYY-MM-DD):",
        font=("Arial", 12)
    ).pack(pady=5)

    date_entry = tk.Entry(
        expense_window,
        width=30
    )
    date_entry.pack(pady=5)

    def save_expense():
        try:
            amount = float(amount_entry.get())
            category = category_box.get()
            description = description_entry.get()
            expense_date = date_entry.get()

            category_id = None

            for category_data in categories:
                if category_data[1] == category:
                    category_id = category_data[0]
                    break

            if category_id is None:
                messagebox.showerror(
                    "Error",
                    "Please select a category."
                )
                return

            add_expense(
                1,
                category_id,
                amount,
                description,
                expense_date
            )

            messagebox.showinfo(
                "Success",
                "Expense added successfully!"
            )

            expense_window.destroy()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount must be a number."
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    add_button = tk.Button(
        expense_window,
        text="Add Expense",
        width=20,
        command=save_expense
    )
    add_button.pack(pady=25)


# Main window - Add Expense
add_button = tk.Button(
    window,
    text="Add Expense",
    width=25,
    height=2,
    command=add_expense_window
)
add_button.pack(pady=10)


# Main window - View Expenses
def show_expenses():
    expenses = get_expenses(1)

    expense_window = tk.Toplevel(window)
    expense_window.title("View Expenses")
    expense_window.geometry("800x400")

    title = tk.Label(
        expense_window,
        text="All Expenses",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=15)

    columns = (
        "ID",
        "Amount",
        "Description",
        "Date",
        "Category"
    )

    table = ttk.Treeview(
        expense_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)

    table.column("ID", width=60)
    table.column("Amount", width=100)
    table.column("Description", width=250)
    table.column("Date", width=120)
    table.column("Category", width=150)

    for expense in expenses:
        table.insert(
            "",
            tk.END,
            values=(
                expense[0],
                f"₹{expense[1]:.2f}",
                expense[2],
                expense[3],
                expense[4]
            )
        )

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

view_button = tk.Button(
    window,
    text="View Expenses",
    width=25,
    height=2,
    command=show_expenses
)

view_button.pack(pady=10)

view_button.pack(pady=10)
def show_total_expenses():
    total = get_total_expense(1)

    messagebox.showinfo(
        "Total Expenses",
        f"Total Expenses: ₹{total:.2f}"
    )
# Main window - Total Expenses
total_button = tk.Button(
    window,
    text="Total Expenses",
    width=25,
    height=2,
    command=show_total_expenses
)

total_button.pack(pady=10)


# Main window - Category Summary
def show_category_summary():
    results = get_category_totals(1)

    if not results:
        messagebox.showinfo(
            "Category Summary",
            "No expenses found."
        )
        return

    summary = ""

    for category, total in results:
        summary += f"{category}: ₹{total:.2f}\n"

    messagebox.showinfo(
        "Category Summary",
        summary
    )
category_button = tk.Button(
    window,
    text="Category Summary",
    width=25,
    height=2,
    command=show_category_summary
)

category_button.pack(pady=10)

# Main window - Exit
exit_button = tk.Button(
    window,
    text="Exit",
    width=25,
    height=2,
    command=window.destroy
)
exit_button.pack(pady=10)


window.mainloop()