<?php
    class NotePad
    {
        const TEXT_SIZE = 20;
        protected $phone;
        public $name;
        public $surname;

        public function __construct($name, $surname, $phone) {
            $this->name = $name;
            $this->surname = $surname;
            $this->phone = $phone;
        }

        public function __clone() {
            $this->name = null;
            $this->surname = null;
            $this->phone = null;
        }
        public function note_show() {
            echo "Имя: $this->name\n", "Фамилия: $this->surname\n", "Номер телефона: $this->phone\n", "Размер текста: ", self::TEXT_SIZE, "\n\n\n";
        }
    }


    class NoteChild extends NotePad
    {
        public function note_show() {
            echo "Название класса: ", __CLASS__, "\n";
            echo "Вызов родительского метода note_show...\n";
            NotePad::note_show();
        }

        public function cut_note() {
                $this->name = mb_substr($this->name, 0, self::TEXT_SIZE);
                $this->surname = mb_substr($this->surname, 0, self::TEXT_SIZE);
                $this->phone = mb_substr($this->phone, 0, self::TEXT_SIZE);
        }
    }


    $note1 = new NotePad("Артем", "Петрушин", "+79116621835");
    $note1->note_show();
    echo "Вывод константы без функции: ", NotePad::TEXT_SIZE, "\n\n\n";

    $note2 = new NotePad("Иван", "Иванов", "+79998887766");
    $note2->note_show();

    $note2_copy = clone $note2;
    $note2_copy->note_show();

    $child1 = new NoteChild("Карина", "Никитина", "+78005553535");
    $child1->note_show();

    $child1_copy = clone $child1;
    $child1_copy->note_show();

    $child2 = new NoteChild("Мария-Антуанетта-Луиза", "де-ла-Сьерра-и-Гонсалес", "+1 (800) 555-0100-1234567");
    $child2->cut_note();
    $child2->note_show();

?>