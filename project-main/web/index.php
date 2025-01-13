<?php
include 'database.php';

try {
    // Connexion à la base de données
    $db = Database::getInstance('mysql', 'comparatordb0', 'user', 'passwordUser0');

    // Initialisation du filtre unique
    $filter = isset($_GET['filter']) ? $_GET['filter'] : '';
    $price_min = isset($_GET['price_min']) && $_GET['price_min'] !== '' ? floatval($_GET['price_min']) : null;
    $price_max = isset($_GET['price_max']) && $_GET['price_max'] !== '' ? floatval($_GET['price_max']) : null;

    // Pagination
    $itemsPerPage = 40;
    $page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
    $offset = ($page - 1) * $itemsPerPage;

    // Récupération des catégories et noms pour le filtre combiné
    $options = $db->query("SELECT DISTINCT category, name FROM articles ORDER BY category, name");

    // Construction de la requête SQL dynamique
    $query = "SELECT * FROM articles WHERE 1=1";
    $params = [];

    if ($filter) {
        list($category, $name) = explode('|', $filter);
        if ($category) {
            $query .= " AND category = ?";
            $params[] = $category;
        }
        if ($name) {
            $query .= " AND name = ?";
            $params[] = $name;
        }
    }

    if ($price_min !== null) {
        $query .= " AND price >= ?";
        $params[] = $price_min;
    }
    if ($price_max !== null) {
        $query .= " AND price <= ?";
        $params[] = $price_max;
    }

    // Ajout de la pagination
    $query .= " ORDER BY price ASC LIMIT $offset, $itemsPerPage";

    // Exécution de la requête
    $games = $db->query($query, $params);

    // Récupération du total pour la pagination
    $countQuery = "SELECT COUNT(*) as total FROM articles WHERE 1=1";
    if ($filter) {
        if ($category) {
            $countQuery .= " AND category = ?";
        }
        if ($name) {
            $countQuery .= " AND name = ?";
        }
    }
    if ($price_min !== null) {
        $countQuery .= " AND price >= ?";
    }
    if ($price_max !== null) {
        $countQuery .= " AND price <= ?";
    }

    $totalItems = $db->query($countQuery, $params)[0]['total'];
    $totalPages = ceil($totalItems / $itemsPerPage);

    // Affichage du formulaire pour le filtre combiné
    echo "<link rel='stylesheet' href='main.css'>";
    echo "<form method='GET' style='text-align:center; margin-bottom:20px;'>";
    echo "Filtrer par : <select name='filter' id='filter'>";
    echo "<option value=''>Tous</option>";

    $currentCategory = '';
    foreach ($options as $option) {
        if ($option['category'] !== $currentCategory) {
            if ($currentCategory !== '') {
                echo "</optgroup>";
            }
            $currentCategory = $option['category'];
            echo "<optgroup label='{$currentCategory}'>";
        }
        $selected = ($filter === "{$option['category']}|{$option['name']}") ? "selected" : "";
        echo "<option value='{$option['category']}|{$option['name']}' $selected>{$option['name']}</option>";
    }
    if ($currentCategory !== '') {
        echo "</optgroup>";
    }

    echo "</select>";
    echo " Prix min : <input type='number' step='0.01' name='price_min' value='" . ($price_min !== null ? htmlspecialchars($price_min) : '') . "'>";
    echo " Prix max : <input type='number' step='0.01' name='price_max' value='" . ($price_max !== null ? htmlspecialchars($price_max) : '') . "'>";
    echo " <button type='submit'>Filtrer</button>";
    echo "</form>";

    // Affichage des résultats
    echo "<div class='container'>";
    if ($games && count($games) > 0) {
        foreach ($games as $game) {
            echo "<div class='card'>";
            echo "<img src='{$game['image']}' alt='{$game['name']}' style='width:100%; height:auto; margin-bottom:10px;'>";
            echo "<h2 class='card__title'>{$game['name']}</h2>";
            echo "<p class='card__price'>{$game['price']} €</p>";
            echo "<p class='card__category'>Catégorie : {$game['category']}</p>";
            echo "<p class='card__site'>Site : {$game['site']}</p>";
            echo "<a href='{$game['url']}' class='card__site--url' target='_blank'>Voir le produit</a>";
            echo "</div>";
        }
    } else {
        echo "<p style='text-align:center; width:100%;'>Aucun résultat trouvé pour cette recherche.</p>";
    }
    echo "</div>";

    // Affichage de la pagination
    echo "<div class='pagination' style='text-align: center; margin-top: 20px;'>";
    if ($page > 1) {
        echo "<a href='?" . http_build_query(array_merge($_GET, ['page' => $page - 1])) . "' class='pagination__link'>« Précédent</a>";
    }

    $maxPagesToShow = 5;
    $startPage = max(1, $page - floor($maxPagesToShow / 2));
    $endPage = min($totalPages, $startPage + $maxPagesToShow - 1);

    if ($startPage > 1) {
        echo "<a href='?" . http_build_query(array_merge($_GET, ['page' => 1])) . "' class='pagination__link'>1</a>";
        if ($startPage > 2) {
            echo "<span class='pagination__dots'>...</span>";
        }
    }

    for ($i = $startPage; $i <= $endPage; $i++) {
        $activeClass = $i == $page ? 'pagination__link--active' : '';
        echo "<a href='?" . http_build_query(array_merge($_GET, ['page' => $i])) . "' class='pagination__link $activeClass'>$i</a>";
    }

    if ($endPage < $totalPages) {
        if ($endPage < $totalPages - 1) {
            echo "<span class='pagination__dots'>...</span>";
        }
        echo "<a href='?" . http_build_query(array_merge($_GET, ['page' => $totalPages])) . "' class='pagination__link'>$totalPages</a>";
    }

    if ($page < $totalPages) {
        echo "<a href='?" . http_build_query(array_merge($_GET, ['page' => $page + 1])) . "' class='pagination__link'>Suivant »</a>";
    }
    echo "</div>";

} catch (Exception $e) {
    echo "Erreur : " . $e->getMessage();
}
?>
