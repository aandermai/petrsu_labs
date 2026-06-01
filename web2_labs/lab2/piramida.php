<?php
$im = imagecreatetruecolor(200, 200); // Создание чёрного изображения

$blue = imagecolorallocate($im, 0, 0, 255); // Создание цвета для изображения
$red = imagecolorallocate($im, 255, 0, 0);
$green = imagecolorallocate($im, 0, 255, 0);

imagefilledrectangle ($im, 85, 117, 115, 147, $blue); //залитый прямоугольник

imagefilledellipse($im, 100, 100, 30, 30, $red); //залитый круг

// массив точек для треугольника
$values = array(
            100,  63,  // Point 1 (x, y)
            85,  83, // Point 2 (x, y)
            115,  83,  // Point 3 (x, y)
            );

// рисование треугольника
imagefilledpolygon($im, $values, 3, $green);

// прорисовка
header("Content-type: image/png");
imagepng($im);

?>


