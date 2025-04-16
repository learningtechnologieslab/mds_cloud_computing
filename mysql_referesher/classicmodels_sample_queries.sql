USE classicmodels;

-- ===============================
-- ClassicModels SQL Practice
-- Topics: SELECT, JOINs, GROUP BY, AGGREGATION, SORTING
-- ===============================

-- Make sure you're using the correct database
USE classicmodels;

-- ===============================
-- SECTION 1: Basic SELECT Queries
-- ===============================

-- 1. List all customers
SELECT * FROM customers;

-- 2. Show the first and last name of all employees
SELECT firstName, lastName FROM employees;

-- 3. Get the product name and price of all products
SELECT productName, buyPrice FROM products;

-- 4. Show all orders placed after 2004
SELECT * FROM orders WHERE orderDate > '2004-12-31';

-- 5. Find customers from USA
SELECT customerName, country FROM customers WHERE country = 'USA';

-- ===============================
-- SECTION 2: INNER JOIN Examples
-- ===============================

-- 1. List all orders with their customer names
SELECT o.orderNumber, c.customerName
FROM orders o
INNER JOIN customers c ON o.customerNumber = c.customerNumber;

-- 2. Show product names in each order
SELECT od.orderNumber, p.productName
FROM orderdetails od
INNER JOIN products p ON od.productCode = p.productCode;

-- 3. List employees and their offices
SELECT e.firstName, e.lastName, o.city
FROM employees e
INNER JOIN offices o ON e.officeCode = o.officeCode;

-- 4. Show customers and their sales reps
SELECT c.customerName, e.firstName AS salesRepFirstName
FROM customers c
INNER JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber;

-- 5. Show orders and the total price for each line item
SELECT od.orderNumber, p.productName, od.quantityOrdered * od.priceEach AS lineTotal
FROM orderdetails od
INNER JOIN products p ON od.productCode = p.productCode;

-- ===============================
-- SECTION 3: LEFT JOIN Examples
-- ===============================

-- 1. List all customers and their sales reps, including those without a sales rep
SELECT c.customerName, e.firstName AS salesRepFirstName
FROM customers c
LEFT JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber;

-- 2. Show all products and their order details (if ordered)
SELECT p.productName, od.orderNumber, od.quantityOrdered
FROM products p
LEFT JOIN orderdetails od ON p.productCode = od.productCode;

-- 3. List all employees and the customers they manage
SELECT e.firstName, e.lastName, c.customerName
FROM employees e
LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber;

-- 4. Show all offices and employees (including offices with no employees)
SELECT o.city, e.firstName
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode;

-- 5. Show all orders and their details (even if no line items yet)
SELECT o.orderNumber, od.productCode
FROM orders o
LEFT JOIN orderdetails od ON o.orderNumber = od.orderNumber;

-- ===============================
-- SECTION 4: RIGHT JOIN Examples
-- ===============================

-- 1. List all products and their suppliers (assuming offices are suppliers here for practice)
SELECT o.city AS supplierCity, p.productName
FROM products p
RIGHT JOIN offices o ON p.productVendor = o.city;

-- 2. Show all employees and the customers they manage
SELECT e.firstName, c.customerName
FROM customers c
RIGHT JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber;

-- 3. List all orders and their customers
SELECT o.orderNumber, c.customerName
FROM customers c
RIGHT JOIN orders o ON c.customerNumber = o.customerNumber;

-- 4. Show all order details and their product names
SELECT od.orderNumber, p.productName
FROM orderdetails od
RIGHT JOIN products p ON od.productCode = p.productCode;

-- 5. Show all offices and employees
SELECT o.city, e.firstName
FROM employees e
RIGHT JOIN offices o ON e.officeCode = o.officeCode;

-- ===============================
-- SECTION 5: FULL OUTER JOIN (Emulated with UNION)
-- ===============================

-- Note: MySQL does not support FULL OUTER JOIN directly, use UNION for simulation

-- 1. Customers with or without payments
SELECT c.customerName, p.amount
FROM customers c
LEFT JOIN payments p ON c.customerNumber = p.customerNumber
UNION
SELECT c.customerName, p.amount
FROM customers c
RIGHT JOIN payments p ON c.customerNumber = p.customerNumber;

-- 2. Products that were or were not ordered
SELECT p.productName, od.orderNumber
FROM products p
LEFT JOIN orderdetails od ON p.productCode = od.productCode
UNION
SELECT p.productName, od.orderNumber
FROM products p
RIGHT JOIN orderdetails od ON p.productCode = od.productCode;

-- 3. Employees and customers they manage (with or without matches)
SELECT e.firstName, c.customerName
FROM employees e
LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
UNION
SELECT e.firstName, c.customerName
FROM employees e
RIGHT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber;

-- 4. Offices and employees (with or without assignments)
SELECT o.city, e.firstName
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
UNION
SELECT o.city, e.firstName
FROM offices o
RIGHT JOIN employees e ON o.officeCode = e.officeCode;

-- 5. Orders and payments by customers
SELECT o.customerNumber, p.amount
FROM orders o
LEFT JOIN payments p ON o.customerNumber = p.customerNumber
UNION
SELECT o.customerNumber, p.amount
FROM orders o
RIGHT JOIN payments p ON o.customerNumber = p.customerNumber;

-- ===============================
-- SECTION 6: GROUP BY and Aggregation
-- ===============================

-- 1. Total number of orders per customer
SELECT customerNumber, COUNT(*) AS orderCount
FROM orders
GROUP BY customerNumber;

-- 2. Average payment per customer
SELECT customerNumber, AVG(amount) AS avgPayment
FROM payments
GROUP BY customerNumber;

-- 3. Total quantity sold per product
SELECT productCode, SUM(quantityOrdered) AS totalSold
FROM orderdetails
GROUP BY productCode;

-- 4. Number of employees per office
SELECT officeCode, COUNT(*) AS numEmployees
FROM employees
GROUP BY officeCode;

-- 5. Total sales per order
SELECT orderNumber, SUM(quantityOrdered * priceEach) AS totalOrderAmount
FROM orderdetails
GROUP BY orderNumber;

-- ===============================
-- SECTION 7: ORDER BY / Sorting
-- ===============================

-- 1. List customers sorted by name
SELECT customerName FROM customers ORDER BY customerName ASC;

-- 2. Show top 10 most expensive products
SELECT productName, buyPrice FROM products ORDER BY buyPrice DESC LIMIT 10;

-- 3. List payments sorted by amount descending
SELECT customerNumber, amount FROM payments ORDER BY amount DESC;

-- 4. Orders sorted by order date
SELECT orderNumber, orderDate FROM orders ORDER BY orderDate;

-- 5. Products sorted by product line then by price
SELECT productLine, productName, buyPrice
FROM products
ORDER BY productLine, buyPrice DESC;
