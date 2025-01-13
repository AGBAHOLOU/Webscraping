<?php
include 'database.php';

$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$limit = 40; 
$offset = ($page - 1) * $limit;

$query = "SELECT * FROM articles LIMIT $limit OFFSET $offset";
$result = $conn->query($query);

$articles = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $articles[] = $row;
    }
}

$total_query = "SELECT COUNT(*) as total FROM articles";
$total_result = $conn->query($total_query);
$total_row = $total_result->fetch_assoc();
$total_articles = $total_row['total'];
$total_pages = ceil($total_articles / $limit);

header('Content-Type: application/json');
echo json_encode([
    'articles' => $articles,
    'total_pages' => $total_pages,
    'current_page' => $page
]);
?>
