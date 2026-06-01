const correctAnswers = {
    "question_1": "2", 
    "question_2": ["0", "1"], 
    "question_3": "1", 
    "question_4": "Рыбин Егор Ильич", 
    "question_5": "0", 
    "question_6_1": "2", 
    "question_6_2": "1", 
    "question_6_3": "3" 
};

function submitTest() {
    const formData = new FormData(document.getElementById('testForm'));
    const question_6 = ["question_6_1", "question_6_2", "question_6_3"];
    let score = 0;
    let feedback = "";

    Object.keys(correctAnswers).forEach((key, index) => {
        const userAnswer = formData.getAll(key);
        const correctAnswer = correctAnswers[key];

        if (Array.isArray(correctAnswer)) {
            if (JSON.stringify(userAnswer.sort()) === JSON.stringify(correctAnswer.sort())) {
                score++;
            } else {
                feedback += `<p>Вопрос ${index + 1}: неправильно</p>`;
            }
        } else if (typeof correctAnswer === "string" && !question_6.includes(key))
            if (userAnswer[0] === correctAnswer) {
                score++;
            } else {
                feedback += `<p>Вопрос ${index + 1}: неправильно</p>`;
            }
        });

    question_6.forEach((subQuestion, subIndex) => {
        const userSubAnswer = formData.get(subQuestion);
        const correctSubAnswer = correctAnswers[subQuestion];
        if (userSubAnswer === correctSubAnswer) {
            score++;
        } else {
            feedback += `<p>Вопрос 6.${subIndex + 1}: неправильно</p>`;
        }
        });

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <p><strong>Результат:</strong> ${score} из ${Object.keys(correctAnswers).length}.</p>
        ${feedback || "<p>You win!</p>"}
    `;
    }
