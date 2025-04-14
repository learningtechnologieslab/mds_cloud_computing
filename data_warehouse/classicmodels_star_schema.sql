
DROP DATABASE IF EXISTS classicmodels_star;
CREATE DATABASE classicmodels_star;

USE classicmodels_star;

# STEP 1 - Create DIMENSION and FACT tables

-- Dimension: Customers
CREATE TABLE dim_customers (
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    customerNumber INT,
    customerName VARCHAR(50),
    contactLastName VARCHAR(50),
    contactFirstName VARCHAR(50),
    phone VARCHAR(50),
    addressLine1 VARCHAR(50),
    addressLine2 VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    postalCode VARCHAR(15),
    country VARCHAR(50),
    salesRepEmployeeNumber INT,
    creditLimit DECIMAL(10,2)
);

-- Dimension: Employees
CREATE TABLE dim_employees (
    employee_key INT PRIMARY KEY AUTO_INCREMENT,
    employeeNumber INT,
    lastName VARCHAR(50),
    firstName VARCHAR(50),
    extension VARCHAR(10),
    email VARCHAR(100),
    officeCode VARCHAR(10),
    reportsTo INT,
    jobTitle VARCHAR(50)
);

-- Dimension: Products
CREATE TABLE dim_products (
    product_key INT PRIMARY KEY AUTO_INCREMENT,
    productCode VARCHAR(15),
    productName VARCHAR(70),
    productLine VARCHAR(50),
    productScale VARCHAR(10),
    productVendor VARCHAR(50),
    productDescription TEXT,
    quantityInStock INT,
    buyPrice DECIMAL(10,2),
    MSRP DECIMAL(10,2)
);

-- Dimension: Offices
CREATE TABLE dim_offices (
    office_key INT PRIMARY KEY AUTO_INCREMENT,
    officeCode VARCHAR(10),
    city VARCHAR(50),
    phone VARCHAR(50),
    addressLine1 VARCHAR(50),
    addressLine2 VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    postalCode VARCHAR(15),
    territory VARCHAR(10)
);

-- Dimension: Dates
CREATE TABLE dim_dates (
    date_key INT PRIMARY KEY AUTO_INCREMENT,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day INT,
    day_of_week VARCHAR(10)
);

-- Fact: Orders
CREATE TABLE fact_orders (
    order_key INT PRIMARY KEY AUTO_INCREMENT,
    orderNumber INT,
    orderDate DATE,
    requiredDate DATE,
    shippedDate DATE,
    status VARCHAR(20),
    comments TEXT,
    customer_key INT,
    employee_key INT,
    product_key INT,
    office_key INT,
    orderLineNumber INT,
    quantityOrdered INT,
    priceEach DECIMAL(10,2),
    total DECIMAL(12,2)
);

# STEP 2 - Populate Dimension Tables

-- Customers
INSERT INTO dim_customers (
    customerNumber, customerName, contactLastName, contactFirstName, phone,
    addressLine1, addressLine2, city, state, postalCode, country,
    salesRepEmployeeNumber, creditLimit
)
SELECT DISTINCT
    customerNumber, customerName, contactLastName, contactFirstName, phone,
    addressLine1, addressLine2, city, state, postalCode, country,
    salesRepEmployeeNumber, creditLimit
FROM classicmodels.customers;

-- Employees
INSERT INTO dim_employees (
    employeeNumber, lastName, firstName, extension, email,
    officeCode, reportsTo, jobTitle
)
SELECT DISTINCT
    employeeNumber, lastName, firstName, extension, email,
    officeCode, reportsTo, jobTitle
FROM classicmodels.employees;

-- Offices
INSERT INTO dim_offices (
    officeCode, city, phone, addressLine1, addressLine2,
    state, country, postalCode, territory
)
SELECT DISTINCT
    officeCode, city, phone, addressLine1, addressLine2,
    state, country, postalCode, territory
FROM classicmodels.offices;

-- Products
INSERT INTO dim_products (
    productCode, productName, productLine, productScale,
    productVendor, productDescription, quantityInStock,
    buyPrice, MSRP
)
SELECT DISTINCT
    p.productCode, p.productName, p.productLine, p.productScale,
    p.productVendor, p.productDescription, p.quantityInStock,
    p.buyPrice, p.MSRP
FROM classicmodels.products p;

-- Dates (from orders)
INSERT INTO dim_dates (full_date, year, quarter, month, day, day_of_week)
SELECT DISTINCT
    orderDate,
    YEAR(orderDate),
    QUARTER(orderDate),
    MONTH(orderDate),
    DAY(orderDate),
    DAYNAME(orderDate)
FROM classicmodels.orders;


# STEP 3 - Load Facts Table

INSERT INTO fact_orders (
    orderNumber, orderDate, requiredDate, shippedDate, status, comments,
    customer_key, employee_key, product_key, office_key,
    orderLineNumber, quantityOrdered, priceEach, total
)
SELECT
    o.orderNumber, o.orderDate, o.requiredDate, o.shippedDate, o.status, o.comments,
    
    (SELECT customer_key FROM dim_customers WHERE customerNumber = o.customerNumber),
    (SELECT employee_key FROM dim_employees WHERE employeeNumber = c.salesRepEmployeeNumber),
    (SELECT product_key FROM dim_products WHERE productCode = od.productCode),
    (SELECT office_key FROM dim_offices WHERE officeCode = e.officeCode),
    
    od.orderLineNumber, od.quantityOrdered, od.priceEach,
    od.quantityOrdered * od.priceEach
FROM classicmodels.orders o
JOIN classicmodels.orderdetails od ON o.orderNumber = od.orderNumber
JOIN classicmodels.customers c ON o.customerNumber = c.customerNumber
JOIN classicmodels.employees e ON c.salesRepEmployeeNumber = e.employeeNumber;
