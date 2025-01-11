<?php
    include 'database.php';
?>
 
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="main.css" rel="stylesheet">
    <title>Comparateur</title>
</head>
<body>
 
    <h1>Comparateur de prix des jeux de société</h1>
 
<?php
 
    // Connect to the database
    $db = Database::getInstance('mysql', 'comparatordb', 'user', 'passwordUser1');
 
    // Select all rows from the game table
    #$games = $db->select('game', '*', '', 'game_name');
    $games = $db->select_games();
    $websites = $db->select('website');
 
 
    /*
    // Print the results
    echo "<table>";
    echo "<tr><th>Nom du jeu</th>";
 
    foreach($websites as $website)
    {
        echo "<th>Prix sur le site ".$website["website_name"]."</th>";
    }
 
    echo "</tr>";
   
    foreach ($games as $game) {
 
        echo '<tr>';
        echo '<td>' . $game['game_name'] . '</td>';
 
        foreach($websites as $website)
        {
            $price = $db->select('price', 'price_value', 'price_idgame = '.$game['idgame'].' and price_idwebsite = '.$website['idwebsite']);
           
            if (empty($price))
            {
                echo '<td> - </td>';
            }
            else
            {
                #print_r($price);
                echo '<td>' .$price[0]["price_value"]. ' € </td>';
            }
        }
       
        echo '</tr>';
       
        //echo '<td>https://' . $game['game_website'] . '</td>';
       
    }
    echo '</table>';
*/
 
?>
 
<?php
    echo "<div class=\"container\">";
    foreach ($games as $game) {
        echo "    <div class=\"card\">";
        echo "        <h2 class=\"card__title\">".$game['game_name']."</h2>";
        echo "        <div class=\"card__site\">";
 
        foreach($websites as $website)
        {
            $price = $db->select('price', '*', 'price_idgame = '.$game['idgame'].' and price_idwebsite = '.$website['idwebsite']);
           
            if (empty($price))
            {
                echo '<td> - </td>';
            }
            else
            {
                echo "<span class=\"card__site--site\"><a href=\"".$price[0]["price_url"]."\" class=\"card__site--url\">".$website['website_name']."</a> : ".$price[0]["price_value"]." €</span>";
            }
        }
 
       
        //echo "            <span class=\"card__site--site\"><a href=\"http://LIEN\" class=\"card__site--url\">SITE</a> : PRIX €</span>";
        //echo "            <span class=\"card__site--site\"><a href=\"http://LIEN\" class=\"card__site--url\">SITE</a> : PRIX €</span>";
        echo "        </div>";
        echo "    </div>";
    }
    echo "</div>";
?>
   
</body>
</html>