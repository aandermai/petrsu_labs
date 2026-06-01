<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $downloadDirectory = 'downloads/';
    $downloadFile = $downloadDirectory . basename($_FILES['file']['name']); 
}

echo $downloadFile;
?>