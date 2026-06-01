// Настройка обработчиков для скрытия ошибок
const errorFields = [
    { inputId: 'name', errorId: 'name-empty-error' },
    { inputId: 'phone', errorId: 'phone-empty-error' },
    { inputId: 'institute', errorIds: ['institute-empty-error', 'institute-list-error'] },
    { inputId: 'course', errorId: 'course-empty-error' },
    { inputId: 'hobby', errorIds: ['hobby-empty-error', 'hobby-list-error']}
];

// Функция проверки пустых полей
function validateInput(value, errorElementId) {    
    const errorElement = document.getElementById(errorElementId);

    if (!value) {
        errorElement.style.display = 'block';
        return false;
    } else {
        errorElement.style.display = 'none'; 
    }
    return true;
}

// Проверка значения поля в datalist
function validateDatalist(inputId, datalistId, errorId) {
    const input = document.getElementById(inputId);
    const datalist = document.getElementById(datalistId);
    const options = Array.from(datalist.options).map(option => option.value);

    if (!options.includes(input.value)) {
        document.getElementById(errorId).style.display = 'block';
        return false;
    }
    document.getElementById(errorId).style.display = 'none';
    return true;
}

// Функция скрытия ошибки
function hideError(inputId, errorId) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);

    input.addEventListener('input', () => {
        if (error.style.display === 'block') {
            error.style.display = 'none';
        }
    });

    input.addEventListener('change', () => {
        if (error.style.display === 'block') {
            error.style.display = 'none';
        }
    });
}

errorFields.forEach(({ inputId, errorId, errorIds }) => {
    if (errorId) hideError(inputId, errorId);
    if (errorIds) {
        errorIds.forEach(error => hideError(inputId, error));
    }
});

// Ограничение значений в поле "курс" при изменении (input)
document.getElementById('course').addEventListener('input', (event) => {
    const input = event.target;
    const value = input.value;

    // Если значение не является числом или выходит за пределы, заменяем его
    if (value && (isNaN(value) || value < 1 || value > 6)) {
        // Применяем ограничение, чтобы значение не выходило за пределы 1-6
        input.value = Math.max(1, Math.min(6, value));
    }
});

// Обработчик для скрытия/отображения поля "Другое"
const hobbyInput = document.getElementById('hobby');
const customHobbyContainer = document.getElementById('custom-hobby-container');
const customHobbyInput = document.getElementById('custom-hobby');

hobby.addEventListener('change', () => {
    if (hobbyInput.value === 'Другое') {
        customHobbyContainer.style.display = 'block';
    } else {
        customHobbyContainer.style.display = 'none';
        customHobbyInput.value = ''; // Сбрасываем значение, если поле скрыто
    } 
});

let phoneCount = 0; // Счётчик количества номеров
const maxPhones = 1; // Максимальное количество номеров
// Функция добавления нового телефона
function AddPhone() {
    if (phoneCount >= maxPhones) return;

    // Создаем контейнер для нового телефона и кнопки
    let phoneContainer = document.createElement('div');
    
    // Создаем новый элемент input
    let newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.id = 'phone_2';
    newInput.name = 'phone[]';  // Добавляем массивный атрибут для имени
    newInput.placeholder = "+7 (xxx) xxx-xx-xx";
    newInput.classList.add('phone-input');  // Добавляем класс для телефонов

    // Создаем кнопку "-" для удаления
    let removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.textContent = '-';
    removeButton.style.backgroundColor = '#f44336';
    removeButton.style.color = 'white';
    removeButton.style.border = 'none';
    removeButton.style.padding = '10px';
    removeButton.style.marginTop = '10px';
    removeButton.style.fontSize = '16px';
    removeButton.style.cursor = 'pointer';
    removeButton.style.borderRadius = '5px';
    removeButton.style.width = '590px';
    
    // Добавляем событие для удаления поля
    removeButton.addEventListener('click', function() {
        phoneContainer.remove();
        phoneCount--;
    });

    // Добавляем input и кнопку в контейнер
    phoneContainer.appendChild(newInput);
    phoneContainer.appendChild(removeButton);
    
    // Добавляем контейнер с полем и кнопкой в основной контейнер
    document.getElementById('new-phone-container').appendChild(phoneContainer);

    phoneCount++;
}

// Функция для открытия модального окна
function openModal() {
    // Получаем введённые данные из формы
    const name = document.getElementById('name').value;
    const institute = document.getElementById('institute').value;
    const course = document.getElementById('course').value;
    const hobby = document.getElementById('hobby').value;
    const customHobby = document.getElementById('custom-hobby').value;
    const phoneInputs = document.querySelectorAll('input[name="phone[]"]'); 
    const phones = Array.from(phoneInputs).map(input => input.value).filter(phone => phone); 

    // Валидация
    if (!validateInput(name, 'name-empty-error')) return;
    if (!validateInput(phones[0], 'phone-empty-error')) return;
    if (!validateInput(institute, 'institute-empty-error')) return;
    if (!validateDatalist('institute', 'institute-list', 'institute-list-error')) return;
    if (!validateInput(course, 'course-empty-error')) return;
    if (!validateInput(hobby, 'hobby-empty-error')) return;
    if(!validateDatalist('hobby', 'hobby-list', 'hobby-list-error')) return;

    // Заполняем данные в модальном окне
    document.getElementById('modal-name').innerText = name;
    document.getElementById('modal-phone').innerText = phones.join(', ');
    document.getElementById('modal-institute').innerText = institute;
    document.getElementById('modal-course').innerText = course;

    if (hobby === "Другое") {
        document.getElementById('modal-hobby').innerText = customHobby;
    } else {
        document.getElementById('modal-hobby').innerText = hobby;
    }

    // Показываем модальное окно
    document.getElementById('modal').style.display = 'flex';
}

// Функция для закрытия модального окна
function closeModal() {
    document.getElementById('modal').style.display = 'none';
}