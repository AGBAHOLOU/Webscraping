<?php
 
class Database
{
    private static $instance;
    private $mysqli;
 
    private function __construct($host, $dbname, $username, $password)
    {
        // Connect to the database
        $this->mysqli = new mysqli($host, $username, $password, $dbname);
        if ($this->mysqli->connect_error) {
            die('Connect Error (' . $this->mysqli->connect_errno . ') ' . $this->mysqli->connect_error);
        }
    }
 
    public static function getInstance($host, $dbname, $username, $password)
    {
        // Double-check to make sure the instance hasn't been created by another thread while we were waiting for the lock
        if (self::$instance === null) {
            self::$instance = new self($host, $dbname, $username, $password);
        }
 
        return self::$instance;
    }
 
 
    public function query($query, $values = [])
    {
        // Prepare and execute the query
        $stmt = $this->mysqli->prepare($query);
        if ($values) {
            $types = str_repeat('s', count($values));
            $stmt->bind_param($types, ...$values);
        }
        $stmt->execute();
 
        // Return the result
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
        // Build the SELECT query
        $query = "SELECT * FROM game where idgame in (select price_idgame from
        (SELECT price_idgame, count(1) FROM comparatordb.price group by price_idgame having count(1) > 2) as a)
        ORDER BY game_name;";
       
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
 
    public function update($table, $values, $where)
    {
        // Build the UPDATE query
        $set = [];
        foreach ($values as $column => $value) {
            $set[] = "$column = ?";
        }
        $set = implode(', ', $set);
        $query = "UPDATE $table SET $set WHERE $where";
 
        // Perform the UPDATE query
        return $this->query($query, array_values($values));
    }
 
    public function delete($table, $where)
    {
        // Build the DELETE query
        $query = "DELETE FROM $table WHERE $where";
 
        // Perform the DELETE query
        return $this->query($query);
    }
 
    public function startTransaction()
    {
        // Start a new transaction
        $this->mysqli->begin_transaction();
    }
 
    public function commitTransaction()
    {
        // Commit the current transaction
        $this->mysqli->commit();
    }
 
    public function rollbackTransaction()
    {
        // Roll back the current transaction
        $this->mysqli->rollback();
    }
}
 
?>