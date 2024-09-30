package dbms_with_java;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

public class MySqlExamples {

	public static void main(String[] args) {
		
		// select();
		insert();
		
		/*
		String sql = "INSERT INTO books (book_id, first_name, last_name, number_of_books, dob) ";
		sql += "VALUES (6, 'Stephen', 'King', 400, '1947-09-21')";
		executeQuery(sql);
		*/
		
		/*
		String sql = "UPDATE books SET last_name = 'SomeGuy' WHERE book_id = 5";
		executeQuery(sql);
		*/
		
		/*
		 * String sql = "DELETE FROM books WHERE book_id = 5";
		 * executeQuery(sql);
		 */
		
		
		
		
		
	}
	
	public static void select() {
		Connection conn = null; // connection object
		String hostName = "143.198.177.53"; // server address + port number
		String dbName = "employees"; // default database name
		String dbUserName = "testUser"; // login name for the database server
		String dbPassword = "testUser123@!@!"; // password for the database server

		String sql = "SELECT * FROM employees LIMIT 50;";

		try {
			// Build connection string
			String mySqlConn = "jdbc:mysql://" + hostName + "/" + dbName + "?user=" + dbUserName + "&password="
					+ dbPassword;

			// Instantiate the MySQL database connector driver
			Class.forName("com.mysql.cj.jdbc.Driver");

			// For older versions of MySQL driver, use the line below
			// Class.forName("com.mysql.jdbc.Driver").newInstance();

			// Connect to the database
			conn = DriverManager.getConnection(mySqlConn);
			try {

				Statement statement = conn.createStatement();
				ResultSet rs = statement.executeQuery(sql); // Return ResultSet
				while (rs.next()) {
					System.out.println("Employee id: " + rs.getInt("emp_no"));
					System.out.println("First name: " + rs.getString("first_name"));
					System.out.println("Last name: " + rs.getString("last_name"));
					System.out.println("_______________________________");
				}
			} catch (Exception e) {
				e.printStackTrace(); // debug
			}
		} catch (Exception e) {
			System.err.print(e.toString());
			System.err.println("Unable to connect to database");
		}
	
	}
	
	public static void insert() {
		Connection conn = null; // connection object
		String hostName = "143.198.177.53"; // server address + port number
		String dbName = "employees"; // default database name
		String dbUserName = "testUser"; // login name for the database server
		String dbPassword = "testUser123@!@!"; // password for the database server

		String sql = "INSERT INTO employees (emp_no, birth_date, first_name, last_name, gender, hire_date) ";
		sql += "VALUES (2, '1960-1-1', 'Bob', 'Smith', 'M', CURDATE());";

		System.out.println(sql);


		try {
			// Build connection string
			String mySqlConn = "jdbc:mysql://" + hostName + "/" + dbName + "?user=" + dbUserName + "&password="
					+ dbPassword;

			// Instantiate the MySQL database connector driver
			Class.forName("com.mysql.cj.jdbc.Driver");

			// For older versions of MySQL driver, use the line below
			// Class.forName("com.mysql.jdbc.Driver").newInstance();

			// Connect to the database
			conn = DriverManager.getConnection(mySqlConn);
			try {

				Statement statement = conn.createStatement();
	            statement.executeUpdate(sql); // execute query
				
			} catch (Exception e) {
				e.printStackTrace(); // debug
			}
		} catch (Exception e) {
			System.err.print(e.toString());
			System.err.println("Unable to connect to database");
		}
	
	}
	
	
	public static void executeQuery(String sql) {
		Connection conn = null; // connection object
		String hostName = "143.198.177.53"; // server address + port number
		String dbName = "employees"; // default database name
		String dbUserName = "testUser"; // login name for the database server
		String dbPassword = "testUser123@!@!"; // password for the database server

		

		System.out.println(sql);


		try {
			// Build connection string
			String mySqlConn = "jdbc:mysql://" + hostName + "/" + dbName + "?user=" + dbUserName + "&password="
					+ dbPassword;

			// Instantiate the MySQL database connector driver
			Class.forName("com.mysql.cj.jdbc.Driver");

			// For older versions of MySQL driver, use the line below
			// Class.forName("com.mysql.jdbc.Driver").newInstance();

			// Connect to the database
			conn = DriverManager.getConnection(mySqlConn);
			try {

				Statement statement = conn.createStatement();
	            statement.executeUpdate(sql); // execute query
				
			} catch (Exception e) {
				e.printStackTrace(); // debug
			}
		} catch (Exception e) {
			System.err.print(e.toString());
			System.err.println("Unable to connect to database");
		}
	
	}

}
