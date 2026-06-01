<html>
    <head>
        <title>Задание 1</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <table>
            <thead>
                <tr>
                    <th>Номер задания</th>
                    <th>Решение</th>
                    <th>Результат</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td class="solution">echo "Переменная a: $a\n", "Переменная fl: $fl\n", "Переменная boo: $boo\n", "Переменная str: $str\n";</td>
                    <td>
                        <pre><?php
                            include_once ("main.php");
                            echo "Переменная a: $a\n", "Переменная fl: $fl\n", "Переменная boo: $boo\n", "Переменная str: $str";
                            ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>2</td>
                    <td class="solution">echo "Результат a + str: " $a + $str;</td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        //echo $a + $str;
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>3</td>
                    <td class="solution">
                        echo "Результат a > str: ", $a > $str, "\n";<br>
                        echo "Результат a < str: ", $a < $str, "\n";<br>
                        echo "Результат a == str: ", $a == $str, "\n";<br>
                        echo "Результат a === str: ", $a === $str;<br>
                    </td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        echo "Результат a > str: ", $a > $str, "\n";
                        echo "Результат a < str: ", $a < $str, "\n";
                        echo "Результат a == str: ", $a == $str, "\n";
                        echo "Результат a === str: ", $a === $str;
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>4</td>
                    <td class="solution">echo "Результат nol == pusto: ", $nol == $pusto, "\n";<br>
                    echo "Результат nol === pusto: ", $nol === $pusto, "\n";<br>
                    </td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        echo "Результат nol == pusto: ", $nol == $pusto, "\n";
                        echo "Результат nol === pusto: ", $nol === $pusto, "\n";
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>5</td>
                    <td class="solution">echo "Вывод s1: $s1\n";<br>
                        echo "Вывод s2: $s2\n";<br>
                    </td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        echo "Вывод s1: $s1\n";
                        echo "Вывод s2: $s2\n";
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>6</td>
                    <td class="solution">echo "mas[one]: ", $mas["one"], "\n";<br>
                        echo "mas[2]: ", $mas[2], "\n";<br>
                        echo "mas[3]: ", $mas[3], "\n";<br>
                    </td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        echo "mas[one]: ", $mas["one"], "\n";
                        echo "mas[2]: ", $mas[2], "\n";
                        echo "mas[3]: ", $mas[3], "\n";
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>7</td>
                    <td class="solution">var_dump($mas)</td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        var_dump($mas);
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>8</td>
                    <td class="solution">echo "Полученная строка: ", implode(";", $mas); </td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        echo "Полученная строка: ", implode(";", $mas);
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>9</td>
                    <td class="solution">$name = "a";<br>
                        echo ${$name};</td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        $name = "a";
                        echo ${$name};
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>10</td>
                    <td class="solution">$ref = &$a;<br>
                    echo "a до изменения: $a\n";<br>
                    $ref = 25;<br>
                    echo "a после изменения: $a";</td>
                    <td>
                        <pre><?php
                        $ref = &$a;
                        echo "a до изменения: $a\n";
                        $ref = 25;
                        echo "a после изменения: $a";
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>11</td>
                    <td class="solution">echo "Значение HOST: ", HOST</td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        echo "Значение HOST: ", HOST;
                         ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>12</td>
                    <td class="solution">$file_list = shell_exec('ls -a');<br>
                        echo $file_list;
                    </td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        $file_list = shell_exec('ls -a');
                        echo $file_list;
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>13</td>
                    <td class="solution">echo "До изменения: ", $str.$nol + 1, "\n";<br>
                    echo "После изменения: ", $str.strval($nol)."1"; </td>
                    <td>
                        <pre><?php
                        echo "До изменения: ", $str.$nol + 1, "\n";
                        echo "После изменения: ", $str.strval($nol)."1";
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>14</td>
                    <td class="solution">echo '&lt;a href="', __FILE__, '"&gt;Ссылка на файл&lt;/a&gt;', "\n";<br>
                    echo "Текущая строка кода: ", __LINE__;</td>
                    <td>
                        <pre><?php
                        include_once ("main.php");
                        shell_exec('cd ../..');
                        $file = __DIR__;
                        echo '<a href="', $file, '">Ссылка на файл</a>', "\n";   
                        echo "Текущая строка кода: ", __LINE__;
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>15</td>
                    <td class="solution">
                        $keys = explode(" ", "каждый охотник желает знать, где сидит фазан");<br>     
                        $values = array("красный", "оранжевый", "желтый", "зелёный", "голубой", "синий", "фиолетовый");<br>
                        $colors = array_combine($keys, $values);<br>
                        asort($colors);<br>
                        echo '&lt;table&gt;';<br>
                        echo '&lt;tr&gt;';<br>
                        foreach ($colors as $keys => $values) {<br>
                            echo '&lt;td&gt;', $keys, '&lt;/td&gt;';<br>
                        }<br>
                        echo '&lt;/tr&gt;';<br>
                        echo '&lt;tr&gt;';<br>
                        foreach ($colors as $values) {<br>
                            echo '&lt;td&gt;', $values,'&lt;/td&gt;';<br>
                        }<br>
                        echo '&lt;/tr&gt;';<br>
                        echo '&lt;/table&gt;';
                    </td>
                    <td>
                        <pre><?php
                        $keys = explode(" ", "каждый охотник желает знать где сидит фазан");
                        $values = array("красный", "оранжевый", "желтый", "зелёный", "голубой", "синий", "фиолетовый");
                        $colors = array_combine($keys, $values);
                        asort($colors);

                        echo '<table class="table-from-15-task">';
                        echo '<tr>';
                        foreach ($colors as $key => $value) {
                            echo '<td>', $key, '</td>';
                        }
                        echo '</tr>';
                        echo '<tr>';
                        foreach ($colors as $value) {
                            echo '<td>', $value,'</td>';
                        }
                        echo '</tr>';
                        echo '</table>';
                        ?></pre>
                    </td>
                </tr>
                <tr>
                    <td>16</td>
                    <td class="solution">
                        function NumberParity(int $number=0) {<br>
                        if ($number % 2 == 0) {<br>
                            echo "$number - чётное число";<br>
                        } else {<br>
                            echo "$number - нечётное число";<br>
                        }<br>
                    }<br>

                        NumberParity(2);<br>
                        NumberParity(3);<br>
                        NumberParity();<br>
                    </td>
                    <td>
                        <pre><?php
                        function NumberParity(int $number=0) {
                            if ($number % 2 == 0) {
                                 echo '<p style="color: green;">', "$number - чётное число\n", '</p>';   
                            } else {
                                 echo '<p style="color: red;">', "$number - нечётное число\n", '</p>';   
                            }
                        }

                        NumberParity(2);
                        NumberParity(3);
                        NumberParity();
                        ?></pre>
                    </td>
                    </tr>
            </tbody>
        </table>
    </body>
</html>