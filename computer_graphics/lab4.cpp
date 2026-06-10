#include "GLUT/include/GL/glut.h"
#include <math.h>

// Количество сегментов флага
const int numSegments = 15;

// Время для анимации
float time = 0.0f;

// Функция для рисования флага
void drawFlag() {
    float segmentWidth = 1.0f / numSegments;  // Ширина одного сегмента флага
    float baseAmplitude = 0.1f;               // Базовая амплитуда колебаний

    glBegin(GL_QUADS); // Используем прямоугольники для флага

    // Координаты для первого сегмента (неподвижный)
    float x1 = -0.5f;  // Левая сторона флага (неподвижная)
    float x2 = x1 + segmentWidth;  // Правая сторона сегмента
    float wave1 = 0.0f;  // Левая сторона неподвижна

    // Начальные координаты левого края флага
    float topLeftY = 0.5f;
    float bottomLeftY = -0.5f;

    for (int i = 0; i < numSegments; ++i) {
        // Амплитуда колебаний увеличивается с каждым сегментом
        float amplitude = baseAmplitude * (i / (float)numSegments);  // Увеличение амплитуды от флагштока

        // Правая сторона сегмента колеблется
        float waveTop = amplitude * sin(time + i * 0.5f);    // Верхний край сегмента
        float waveBottom = amplitude * sin(time + i * 0.5f); // Нижний край сегмента

        // Рисуем сегмент флага
        glColor3f(0.0f, 0.6f, 0.3f); // Цвет флага

        // Верхняя и нижняя левая точки (левая сторона сегмента)
        glVertex2f(x1, topLeftY + wave1);        // Верхний левый угол
        glVertex2f(x2, topLeftY + waveTop);      // Верхний правый угол
        glVertex2f(x2, bottomLeftY + waveBottom); // Нижний правый угол
        glVertex2f(x1, bottomLeftY + wave1);     // Нижний левый угол

        // Перемещаем левую сторону на позицию правой для следующего сегмента
        x1 = x2;
        x2 += segmentWidth;

        // Обновляем значение волны для следующего сегмента
        wave1 = waveTop;
    }

    glEnd();
    time += 0.05f;
    if (time > 3.14152f * 2) time = 0;
}

// Функция отображения
void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    // Рисуем флаг
    drawFlag();

    glutSwapBuffers();
}

// Инициализация OpenGL
void init() {
    glClearColor(0.0, 0.0, 0.0, 0.0); // Цвет фона
    glEnable(GL_DEPTH_TEST);          // Включаем тест глубины
}

// Основная функция
int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    glutCreateWindow("Флаг с фиксированным сегментом");

    init();

    glutDisplayFunc(display);
    //glutTimerFunc(16, timer, 0);
    glutIdleFunc(display);

    glutMainLoop();
    return 0;
}
