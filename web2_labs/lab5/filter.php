<?php
    session_start();
    if ($_SESSION['logged_in'] != true) {
        header("Location: login.php");
        exit;
    }

    if ($_SERVER['REQUEST_METHOD'] == "POST") {
        $file = $_FILES['file']['tmp_name'];
        $filter = $_POST["filter"];
        echo $file, '<br>', $filter;
        echo gd_info();
    }

    switch ($filter) {
        case "negative":
            imagefilter($image, IMG_FILTER_NEGATE);
            break;
        case "sepia":
            imagefilter($image, IMG_FILTER_MEAN_REMOVAL);
            break;
        case "black-white":
            imagefilter($image, IMG_FILTER_GRAYSCALE);
            break;

    }

?>