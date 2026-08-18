import mysql.connector
import hashlib

# DATABASE CONNECTION
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="expense_tracker"
    )

# REGISTER USER
def register_user(name, username, email, password):
    connection = get_connection()
    cursor = connection.cursor()
    password_hash = hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

    query = """
    INSERT INTO users
    (name, username, email, password)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (
            name,
            username,
            email,
            password_hash
        )
    )

    connection.commit()
    cursor.close()
    connection.close()

# LOGIN USER
def login_user(login_value, password):
    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

    query = """
    SELECT user_id, name, username, email
    FROM users
    WHERE (username = %s OR email = %s)
    AND password = %s
    """

    cursor.execute(
        query,
        (
            login_value,
            login_value,
            password_hash
        )
    )

    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

# ADD EXPENSE

def add_expense(
    user_id,
    category_id,
    amount,
    description,
    expense_date
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO expenses
    (user_id, category_id, amount, description, expense_date)
    VALUES (%s, %s, %s, %s, %s)
    """

    data = (
        user_id,
        category_id,
        amount,
        description,
        expense_date
    )
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()

# GET EXPENSES
def get_expenses(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
    SELECT
        e.expense_id,
        e.amount,
        e.description,
        e.expense_date,
        c.category_name
    FROM expenses e
    JOIN categories c
        ON e.category_id = c.category_id
    WHERE e.user_id = %s
    ORDER BY e.expense_id DESC
    """
    cursor.execute(query, (user_id,))
    expenses = cursor.fetchall()
    cursor.close()
    connection.close()
    return expenses

# UPDATE EXPENSE
def update_expense(expense_id, amount, description):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE expenses
    SET amount = %s,
        description = %s
    WHERE expense_id = %s
    """

    cursor.execute(
        query,
        (
            amount,
            description,
            expense_id
        )
    )
    connection.commit()
    cursor.close()
    connection.close()

# DELETE EXPENSE
def delete_expense(expense_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
    DELETE FROM expenses
    WHERE expense_id = %s
    """
    cursor.execute(
        query,
        (expense_id,)
    )
    connection.commit()
    cursor.close()
    connection.close()

# TOTAL EXPENSE
def get_total_expense(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
    SELECT SUM(amount)
    FROM expenses
    WHERE user_id = %s
    """

    cursor.execute(
        query,
        (user_id,)
    )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] or 0

# CATEGORY TOTALS
def get_category_totals(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        c.category_name,
        SUM(e.amount) AS total_amount
    FROM expenses e
    JOIN categories c
        ON e.category_id = c.category_id
    WHERE e.user_id = %s
    GROUP BY c.category_name
    """

    cursor.execute(
        query,
        (user_id,)
    )
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

# GET CATEGORIES
def get_categories():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT category_id, category_name
    FROM categories
    ORDER BY category_id
    """
    cursor.execute(query)
    categories = cursor.fetchall()
    cursor.close()
    connection.close()
    return categories
