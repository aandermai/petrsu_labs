<?php

$im = imagecreatefromjpeg("./cat.jpg");

imagefilter($im, IMG_FILTER_GRAYSCALE);

// устанавливаем тип содержимого
header('content-type: image/jpeg');


// вывод изображения на экран
imagejpeg($im);

// очистка памяти
imagedestroy($im);

?>
