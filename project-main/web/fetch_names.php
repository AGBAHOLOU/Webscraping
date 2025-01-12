<?php
include 'database.php';

header('Content-Type: application/json');

try {
    // Connexion à la base de données
    $db = Database::getInstance('bdd', 'comparatordb0', 'user', 'passwordUser0');

    // Récupération de la catégorie depuis la requête GET
    $category = isset($_GET['category']) ? $_GET['category'] : '';

    // Récupération des noms en fonction de la catégorie
    if ($category) {
        $query = "SELECT DISTINCT name FROM articles WHERE category = ?";
        $names = $db->query($query, [$category]);
        echo json_encode($names);
    } else {
        echo json_encode([]);
    }
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
?>
