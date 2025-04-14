
DROP DATABASE IF EXISTS classicmodels_snowflake;
CREATE DATABASE classicmodels_snowflake;

USE classicmodels_snowflake;

-- DIMENSION TABLES

CREATE TABLE dim_date (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE,
    required_date DATE,
    shipped_date DATE
);

CREATE TABLE dim_office (
    office_code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(50),
    phone VARCHAR(50),
    address_line1 VARCHAR(100),
    address_line2 VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50),
    postal_code VARCHAR(20),
    territory VARCHAR(50)
);

CREATE TABLE dim_employee (
    employee_number INT PRIMARY KEY,
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    email VARCHAR(100),
    office_code VARCHAR(10),
    reports_to INT,
    FOREIGN KEY (office_code) REFERENCES dim_office(office_code)
);

CREATE TABLE dim_productline (
    product_line VARCHAR(50) PRIMARY KEY,
    text_description TEXT,
    html_description TEXT,
    image BLOB
);

CREATE TABLE dim_product (
    product_code VARCHAR(15) PRIMARY KEY,
    product_name VARCHAR(70),
    product_line VARCHAR(50),
    product_scale VARCHAR(10),
    product_vendor VARCHAR(50),
    product_description TEXT,
    quantity_in_stock INT,
    buy_price DECIMAL(10,2),
    MSRP DECIMAL(10,2),
    FOREIGN KEY (product_line) REFERENCES dim_productline(product_line)
);

CREATE TABLE dim_customer (
    customer_number INT PRIMARY KEY,
    customer_name VARCHAR(50),
    contact_last_name VARCHAR(50),
    contact_first_name VARCHAR(50),
    phone VARCHAR(50),
    address_line1 VARCHAR(100),
    address_line2 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(15),
    country VARCHAR(50),
    sales_rep_employee_number INT,
    FOREIGN KEY (sales_rep_employee_number) REFERENCES dim_employee(employee_number)
);

CREATE TABLE dim_payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_number INT,
    check_number VARCHAR(50),
    payment_date DATE,
    amount DECIMAL(10,2),
    FOREIGN KEY (customer_number) REFERENCES dim_customer(customer_number)
);

-- FACT TABLE

CREATE TABLE fact_sales (
    order_number INT,
    product_code VARCHAR(15),
    quantity_ordered INT,
    price_each DECIMAL(10,2),
    order_line_number SMALLINT,
    order_date DATE,
    required_date DATE,
    shipped_date DATE,
    customer_number INT,
    PRIMARY KEY (order_number, product_code),
    FOREIGN KEY (product_code) REFERENCES dim_product(product_code),
    FOREIGN KEY (customer_number) REFERENCES dim_customer(customer_number)
);


# PART 2 - Migration Queries

-- Insert into dim_office
INSERT INTO dim_office
SELECT * FROM classicmodels.offices;

-- Insert into dim_employee
INSERT INTO dim_employee (employee_number, last_name, first_name, email, office_code, reports_to)
SELECT employeeNumber, lastName, firstName, email, officeCode, reportsTo FROM classicmodels.employees;

-- Insert into dim_productline
INSERT INTO dim_productline (product_line, text_description, html_description, image)
SELECT productLine, textDescription, htmlDescription, image FROM classicmodels.productlines;

-- Insert into dim_product
INSERT INTO dim_product (product_code, product_name, product_line, product_scale, product_vendor,
                         product_description, quantity_in_stock, buy_price, MSRP)
SELECT productCode, productName, productLine, productScale, productVendor,
       productDescription, quantityInStock, buyPrice, MSRP FROM classicmodels.products;

-- Insert into dim_customer
INSERT INTO dim_customer (customer_number, customer_name, contact_last_name, contact_first_name,
                          phone, address_line1, address_line2, city, state, postal_code, country, sales_rep_employee_number)
SELECT customerNumber, customerName, contactLastName, contactFirstName,
       phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber FROM classicmodels.customers;

-- Insert into dim_payment
INSERT INTO dim_payment (customer_number, check_number, payment_date, amount)
SELECT customerNumber, checkNumber, paymentDate, amount FROM classicmodels.payments;

-- Insert into fact_sales
INSERT INTO fact_sales (order_number, product_code, quantity_ordered, price_each, order_line_number,
                        order_date, required_date, shipped_date, customer_number)
SELECT o.orderNumber, od.productCode, od.quantityOrdered, od.priceEach, od.orderLineNumber,
       o.orderDate, o.requiredDate, o.shippedDate, o.customerNumber
FROM classicmodels.orders o
JOIN classicmodels.orderdetails od ON o.orderNumber = od.orderNumber;
