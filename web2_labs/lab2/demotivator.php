<?php

// тип содержимого - jpg
header('Content-Type: image/jpeg');

// открытие файла с картинкой и связываем его с идентификатором $im
$im = imagecreatefromjpeg("./1.jpg");

// подгрузка шрифта
$font = './arial.ttf';

// создание цвета текста
$text_color = imagecolorallocate($im, 255, 255, 255);

// прорисовка строки текста шрифтом (латиница!) 5 в координаты 5, 5
//imagestring($im, 5, 65, 380, "yay", $text_color);
imagettftext($im, 36, 0, 65, 380, $text_color, $font, "ЕГЭ ПО РИСОВАНИЮ");

// вывод изображения в браузер
imagejpeg($im);

imagedestroy($im);
?>
