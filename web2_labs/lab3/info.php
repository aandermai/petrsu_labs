<html>
    <head>
        <title>Информация</title>
    </head>
    <body>
        <?php
        echo "Информация о пользователе: ",  `id`, '<br>';
        echo "Имя Web-сервера: ", $_SERVER['SERVER_NAME'], '<br>' ;
        echo "Версия браузера: ", $_SERVER['HTTP_USER_AGENT'], '<br>';
        echo "Страница, с которой был переход: ", $_SERVER['HTTP_REFERER'], '<br>';
        ?>
        <a href="./login.php">Возврат прежней страницы</a>

    </body>
</html>


