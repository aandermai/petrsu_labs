<html>
    <head>
        <title>Авторизация</title>
        <style>
            body {
                    position: relative;
            }

            input {
                    position: relative;
                    display: flex;
                    margin-bottom: 20px;
                    border-radius: 10px;
            }

            .button {
                    height: 25px;
                    width: 170px;
            }
        </style>
    </head>
    <body>
        <h1>Форма получения доступа к третьей лабораторной работе</h1>
        <form action="" method="post">
            Логин
            <input type="text" name="login" value="<?php if (isset($_POST['login'])) echo $_POST['login'] ?>">
            Пароль
            <input type="password" name="password">
            <input class="button" type="submit" value="Вывести">
        </form>
        <?php
            if (isset($_POST['login']) && isset($_POST['password'])) {
                $login = $_POST['login'];
                $password = $_POST['password'];
                if (($login != "user" || $password != "qwerty") || (empty($login) || empty($password)))  {
                    echo "Неправильный логин или пароль. Попробуйте ещё раз.";
                } else {
                    include("./info.php");
                }
            }
        ?>
    </body>
</html>