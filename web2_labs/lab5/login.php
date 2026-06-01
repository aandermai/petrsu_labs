<?php
    session_start();
    if (isset($_POST['login']) && isset($_POST['password'])) {
        $login = $_POST['login'];
        $password = $_POST['password'];
        if ($login != "user" || $password != "qwerty")  {
            echo "Неправильный логин или пароль. Попробуйте ещё раз.";
        } else {
            $_SESSION['logged_in'] = true;
            header("Location: upload.php");
            exit;
        }
    }
?>

<html>
    <head>
        <title>Filter.io: Авторизация</title>
        <link rel=stylesheet href="./style.css">
    </head>
    <body>
        <h1>Filter.io</h1>
        <form action="" method="post">
            Логин
            <input type="text" name="login" value="<?php if (isset($_POST['login'])) echo $_POST['login'] ?>">
            Пароль
            <input type="password" name="password">
            <input class="button" type="submit" value="Вывести">
        </form>
    </body>
</html>
