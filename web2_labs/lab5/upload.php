<?php
    session_start();
    if ($_SESSION['logged_in'] != true) {
        header("Location: login.php");
        exit;
    }
?>
<html>
    <head>
        <title>Filter.io: Загрузка изображения</title>
        <link rel=stylesheet href="./upload-style.css">
    </head>
    <body>    
        <form action="filter.php" method="post" enctype="multipart/form-data">
            <div>
                <p>Выберите фото</p>
                <input type="file" name="file" multiple>
            </div>
            <div>
                <p>Выберите обработку</p>
                <input type="radio" id="filterChoice1" name="filter" value="negative" checked>
                <label for="negative">Негатив</label><br>

                <input type="radio" id="filterChoice2" name="filter" value="sepia">
                <label for="sepia">Сепия</label><br>

                <input type="radio" id="filterChoice3" name="filter" value="black-white">
                <label for="black-white">ЧБ</label><br>
            </div>
            <div>
                <input type="submit" value="Применить">
            </div>
        </form>
    </body>
</html>
