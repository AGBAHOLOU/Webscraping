<?php
include 'database.php';

try {
    // Connexion à la base de données
    $db = Database::getInstance('bdd', 'comparatordb0', 'user', 'passwordUser0');

    // Initialisation des filtres
    $category = isset($_GET['category']) ? $_GET['category'] : '';
    $name = isset($_GET['name']) ? $_GET['name'] : '';
    $price_min = isset($_GET['price_min']) && $_GET['price_min'] !== '' ? floatval($_GET['price_min']) : null;
    $price_max = isset($_GET['price_max']) && $_GET['price_max'] !== '' ? floatval($_GET['price_max']) : null;

    // Récupération des catégories pour la liste déroulante
    $categories = $db->query("SELECT DISTINCT category FROM articles");

    // Récupération des noms correspondant à la catégorie sélectionnée
    $names = [];
    if ($category) {
        $names = $db->query("SELECT DISTINCT name FROM articles WHERE category = ?", [$category]);
    }

    // Construction de la requête SQL dynamique
    $query = "SELECT * FROM articles WHERE 1=1";
    $params = [];

    if ($category) {
        $query .= " AND category = ?";
        $params[] = $category;
    }
    if ($name) {
        $query .= " AND name = ?";
        $params[] = $name;
    }
    if ($price_min !== null) {
        $query .= " AND price >= ?";
        $params[] = $price_min;
    }
    if ($price_max !== null) {
        $query .= " AND price <= ?";
        $params[] = $price_max;
    }

    // Ajout du tri par prix croissant
    $query .= " ORDER BY price ASC";

    // Exécution de la requête
    $games = $db->query($query, $params);

    // Affichage du formulaire pour les filtres
    echo "<link rel='stylesheet' href='main.css'>";
    echo "<form method='GET' style='text-align:center; margin-bottom:20px;'>";
    echo "Catégorie : <select name='category' id='category'>";
    echo "<option value=''>Toutes</option>";
    foreach ($categories as $cat) {
        $selected = ($cat['category'] === $category) ? "selected" : "";
        echo "<option value='{$cat['category']}' $selected>{$cat['category']}</option>";
    }
    echo "</select>";

    echo " Nom : <select name='name' id='name'>";
    echo "<option value=''>Tous</option>";
    foreach ($names as $n) {
        $selected = ($n['name'] === $name) ? "selected" : "";
        echo "<option value='{$n['name']}' $selected>{$n['name']}</option>";
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
} catch (Exception $e) {
    echo "Erreur : " . $e->getMessage();
}
?>

<script>
// JavaScript pour mettre à jour la liste des noms dynamiquement
document.getElementById('category').addEventListener('change', function () {
    const category = this.value;
    const nameSelect = document.getElementById('name');

    // Réinitialisation des options
    nameSelect.innerHTML = "<option value=''>Tous</option>";

    // Appel AJAX pour récupérer les noms
    if (category) {
        fetch(`fetch_names.php?category=${category}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(name => {
                    const option = document.createElement('option');
                    option.value = name.name;
                    option.textContent = name.name;
                    nameSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Erreur:', error));
    }
});
</script>
