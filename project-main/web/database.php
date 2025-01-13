<?php

class Database {
    private static $instance = null;
    private $connection;

    // Constructeur privé pour le singleton
    private function __construct($host, $dbname, $username, $password) {
        $this->connection = new mysqli($host, $username, $password, $dbname);

        if ($this->connection->connect_error) {
            die("Erreur de connexion : " . $this->connection->connect_error);
        }
    }

    // Méthode pour récupérer l'instance unique
    public static function getInstance($host, $dbname, $username, $password) {
        if (self::$instance === null) {
            self::$instance = new Database($host, $dbname, $username, $password);
        }
        return self::$instance;
    }

    // Méthode pour exécuter une requête
    public function query($sql, $params = []) {
        $stmt = $this->connection->prepare($sql);

        if ($params) {
            $types = str_repeat('s', count($params));
            $stmt->bind_param($types, ...$params);
        }

        $stmt->execute();
        $result = $stmt->get_result();

        if ($result) {
            return $result->fetch_all(MYSQLI_ASSOC);
        }

        return [];
    }
}
?>
