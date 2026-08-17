CREATE DATABASE expense_tracker;
USE expense_tracker;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SHOW TABLES;

CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

SHOW TABLES;

CREATE TABLE expenses (
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255),
    expense_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

SHOW TABLES;

INSERT INTO categories (category_name)
VALUES
('Food'),
('Travel'),
('Shopping'),
('Bills'),
('Entertainment'),
('Education'),
('Healthcare'),
('Other');

SELECT * FROM categories;

INSERT INTO users (name, email, password)
VALUES
('Omkar', 'omkar@example.com', 'test123');
SELECT * FROM users;

INSERT INTO expenses
(user_id, category_id, amount, description, expense_date)
VALUES
(1, 1, 120.00, 'Lunch', '2026-08-13'),
(1, 2, 80.00, 'Bus ticket', '2026-08-12'),
(1, 3, 500.00, 'T-shirt', '2026-08-10'),
(1, 4, 1200.00, 'Electricity bill', '2026-08-05');

SELECT * FROM expenses;

SELECT
    e.expense_id,
    e.amount,
    e.description,
    e.expense_date,
    c.category_name
FROM expenses e
JOIN categories c
    ON e.category_id = c.category_id
WHERE e.user_id = 1;

SELECT SUM(amount) AS total_expense
FROM expenses
WHERE user_id = 1;

SELECT
    c.category_name,
    SUM(e.amount) AS total_amount
FROM expenses e
JOIN categories c
    ON e.category_id = c.category_id
WHERE e.user_id = 1
GROUP BY c.category_name;

UPDATE expenses
SET amount = 150.00,
    description = 'Lunch + cold drink'
WHERE expense_id = 1;
SELECT * FROM expenses
WHERE expense_id = 1;

DELETE FROM expenses
WHERE expense_id = 4;
SELECT * FROM expenses;

SELECT * FROM expenses;

USE expense_tracker;

SELECT *
FROM expenses
ORDER BY expense_id DESC;

USE expense_tracker;

USE expense_tracker;

ALTER TABLE users
ADD COLUMN username VARCHAR(50) NOT NULL UNIQUE AFTER name;

DESCRIBE users;
