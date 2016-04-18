<?php

// Code to query an SQLite database and return
// results as JSON.

// Specify your sqlite database name and path //

$dir = 'sqlite:dublinbikes_test_database.db';

// Instantiate PDO connection object and failure msg //
$dbh = new PDO($dir) or die("cannot open database");

// Define your SQL statement //
$query = SELECT *
FROM Dynamic_Data
ORDER by Timestamp desc limit 101;






// Iterate through the results and pass into JSON encoder //
foreach ($dbh->query($query) as $row) {
echo json_encode($row[0]);

$dir = NULL;
}
?>

