<?php

class Database
{
    private static $instance;
    private $mysqli;

    private function __construct($host, $dbname, $username, $password)
    {
        // Enable detailed error reporting for debugging
        mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

        // Connect to the database using TCP/IP to avoid socket issues
        $this->mysqli = new mysqli($host, $username, $password, $dbname);

        // Check for connection errors
        if ($this->mysqli->connect_error) {
            die('Connect Error (' . $this->mysqli->connect_errno . ') ' . $this->mysqli->connect_error);
        }
    }

    public static function getInstance($host, $dbname, $username, $password)
    {
        // Create an instance if it doesn't exist
        if (self::$instance === null) {
            self::$instance = new self($host, $dbname, $username, $password);
        }

        return self::$instance;
    }

    public function query($query, $values = [])
    {
        // Prepare the query
        $stmt = $this->mysqli->prepare($query);
        if (!$stmt) {
            die('Query preparation error: ' . $this->mysqli->error);
        }

        // Bind parameters if they exist
        if ($values) {
            $types = str_repeat('s', count($values));
            $stmt->bind_param($types, ...$values);
        }

        // Execute the statement
        $stmt->execute();

        // Fetch the result
        $result = $stmt->get_result();
        if ($result === false) {
            // Return the number of rows affected for non-SELECT queries
            return $stmt->affected_rows;
        } else {
            // Return the fetched rows for SELECT queries
            return $result->fetch_all(MYSQLI_ASSOC);
        }
    }

    public function select($table, $columns = '*', $where = '', $orderby = '')
    {
        // Build the SELECT query
        $query = "SELECT $columns FROM $table";
        if ($where != '') {
            $query .= " WHERE $where";
        }

        if ($orderby != '') {
            $query .= " ORDER BY $orderby";
        }

        // Perform the SELECT query
        return $this->query($query);
    }

    public function select_games()
    {
        // Correct the SQL query based on your database structure
        $query = "
        SELECT *
        FROM articles
        ORDER BY name
        ";

        // Perform the SELECT query
        return $this->query($query);
    }

    public function insert($table, $values)
    {
        // Build the INSERT query
        $columns = implode(', ', array_keys($values));
        $placeholders = '?' . str_repeat(', ?', count($values) - 1);
        $query = "INSERT INTO $table ($columns) VALUES ($placeholders)";

        // Perform the INSERT query
        return $this->query($query, array_values($values));
    }
}

?>