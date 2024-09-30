#install.packages("RMySQL")
library(RMySQL)

# Connecting to MySQL:
# Once the RMySQL library is installed create a database connection object.
conn = dbConnect(MySQL(), user='testUser', password='testUser123@!@!', dbname='employees', host='143.198.177.53')
dbListTables(conn)


# SELECT
rs = dbSendQuery(conn, "SELECT * FROM employees LIMIT 50");
data.frame = fetch(rs)
head(data.frame)


# INSERT
sql <- "INSERT INTO employees.employees (emp_no, birth_date, first_name, last_name, gender, hire_date) VALUES (8, '1960-1-1', 'Bob', 'Smith', 'M', CURDATE());";
dbSendQuery(conn,sql)


# UPDATE
sql <- "UPDATE employees.employees SET last_name = 'Johnson' WHERE emp_no = 8;";
dbSendQuery(conn,sql)

# DELETE
sql <- "DELETE FROM employees.employees WHERE emp_no = 8;";
dbSendQuery(conn,sql)



