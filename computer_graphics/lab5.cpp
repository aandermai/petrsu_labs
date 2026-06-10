#include "GLUT/include/GL/glut.h"
#include <math.h>

#define PI 3.14159265

// Параметры для орбит планет
float angleMercury = 0.0f;
float angleVenus = 0.0f;
float angleEarth = 0.0f;
float angleMars = 0.0f;
float angleJupiter = 0.0f;
float angleSaturn = 0.0f;
float angleUranus = 0.0f;
float angleNeptune = 0.0f;

float sunRadius = 1.5f;
float mercuryOrbitRadius = 2.0f, mercuryRadius = 0.2f;
float venusOrbitRadius = 3.0f, venusRadius = 0.3f;
float earthOrbitRadius = 5.0f, earthRadius = 0.5f;
float marsOrbitRadius = 7.0f, marsRadius = 0.4f;
float jupiterOrbitRadius = 10.0f, jupiterRadius = 0.9f;
float saturnOrbitRadius = 13.0f, saturnRadius = 0.8f;
float uranusOrbitRadius = 15.0f, uranusRadius = 0.6f;
float neptuneOrbitRadius = 17.0f, neptuneRadius = 0.6f;

// Параметры для спутника Земли
float moonOrbitRadius = 1.0f; // Радиус орбиты спутника
float moonRadius = 0.1f; // Радиус спутника
float angleMoon = 0.0f; // Угол орбиты спутника

void setupLighting() {
    // Установка источника света
    GLfloat light_position[] = { 0.0f, 0.0f, 0.0f, 1.0f }; // Положение света (центр)
    GLfloat light_ambient[] = { 0.2f, 0.2f, 0.2f, 1.0f }; // Рассеянный свет, который равномерно освещает все объекты в сцене
    GLfloat light_diffuse[] = { 1.0f, 1.0f, 1.0f, 1.0f }; // Свет, который рассеивается на поверхности объекта
    GLfloat light_specular[] = { 1.0f, 1.0f, 1.0f, 1.0f }; // Свет, который отражается от зеркальных поверхностей

    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);
    glLightfv(GL_LIGHT0, GL_POSITION, light_position);
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
}

void drawSphere(float radius) {
    glutSolidSphere(radius, 30, 30);
}

void drawOrbit(float radius) {
    glPushMatrix();
    glColor3f(1.0f, 1.0f, 1.0f); // Белый цвет для орбиты
    glBegin(GL_LINE_LOOP); // Рисуем окружность
    for (int i = 0; i < 360; i++) {
        float angle = i * PI / 180.0f;
        float x = radius * cos(angle);
        float z = radius * sin(angle);
        glVertex3f(x, 0.0f, z); // Вычисление точек окружности
    }
    glEnd();
    glPopMatrix();
}

void drawPlanet(float orbitRadius, float planetRadius, float angle, const GLfloat color[4]) {
    // Расчет позиции планеты на орбите с учетом текущего угла
    float x = orbitRadius * cos(angle * PI / 180.0); // X-координата
    float z = orbitRadius * sin(angle * PI / 180.0); // Z-координата

    glPushMatrix();
    glTranslatef(x, 0.0f, z); // Перемещение планеты на орбиту
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color); // Задание цвета
    drawSphere(planetRadius); // Отрисовка планеты
    glPopMatrix();
}

void drawMoon(float earthX, float earthZ) {
    // Позиция спутника относительно Земли
    float x = earthX + moonOrbitRadius * cos(angleMoon * PI / 180.0f);
    float z = earthZ + moonOrbitRadius * sin(angleMoon * PI / 180.0f);

    glPushMatrix();
    glTranslatef(x, 0.0f, z); // Перемещение на орбиту спутника
    GLfloat moonColor[] = { 0.8f, 0.8f, 0.8f, 1.0f }; // Цвет спутника
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, moonColor);
    drawSphere(moonRadius); // Отрисовка спутника
    glPopMatrix();
}

void drawSolarSystem() {
    // Солнце в центре
    glPushMatrix();
    GLfloat sunColor[] = { 1.0f, 1.0f, 1.0f, 1.0f }; // Белый цвет для солнца
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, sunColor);
    drawSphere(sunRadius);
    glPopMatrix();

    // Орбиты
    drawOrbit(mercuryOrbitRadius);
    drawOrbit(venusOrbitRadius);
    drawOrbit(earthOrbitRadius);
    drawOrbit(marsOrbitRadius);
    drawOrbit(jupiterOrbitRadius);
    drawOrbit(saturnOrbitRadius);
    drawOrbit(uranusOrbitRadius);
    drawOrbit(neptuneOrbitRadius);

    // Планеты
    GLfloat mercuryColor[] = { 0.7f, 0.7f, 0.5f, 1.0f };
    drawPlanet(mercuryOrbitRadius, mercuryRadius, angleMercury, mercuryColor);

    GLfloat venusColor[] = { 0.9f, 0.6f, 0.3f, 1.0f };
    drawPlanet(venusOrbitRadius, venusRadius, angleVenus, venusColor);

    GLfloat earthColor[] = { 0.0f, 0.0f, 1.0f, 1.0f };
    drawPlanet(earthOrbitRadius, earthRadius, angleEarth, earthColor);

    GLfloat marsColor[] = { 1.0f, 0.0f, 0.0f, 1.0f };
    drawPlanet(marsOrbitRadius, marsRadius, angleMars, marsColor);

    GLfloat jupiterColor[] = { 0.9f, 0.6f, 0.3f, 1.0f };
    drawPlanet(jupiterOrbitRadius, jupiterRadius, angleJupiter, jupiterColor);

    GLfloat saturnColor[] = { 0.9f, 0.8f, 0.5f, 1.0f };
    drawPlanet(saturnOrbitRadius, saturnRadius, angleSaturn, saturnColor);

    GLfloat uranusColor[] = { 0.5f, 0.8f, 1.0f, 1.0f };
    drawPlanet(uranusOrbitRadius, uranusRadius, angleUranus, uranusColor);

    GLfloat neptuneColor[] = { 0.3f, 0.3f, 0.9f, 1.0f };
    drawPlanet(neptuneOrbitRadius, neptuneRadius, angleNeptune, neptuneColor);

    // Спутник Земли
    GLfloat earthX = earthOrbitRadius * cos(angleEarth * PI / 180.0f);
    GLfloat earthZ = earthOrbitRadius * sin(angleEarth * PI / 180.0f);
    drawMoon(earthX, earthZ); // Отрисовка спутника
}


void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();

    // Камера
    gluLookAt(0.0f, 15.0f, 30.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f);

    setupLighting();
    drawSolarSystem();

    glutSwapBuffers();
}

float speedFactor = 0.1f; // Коэффициент скорости

void update() {
    // Обновление углов орбит для анимации
    angleMercury += 4.0f * speedFactor;
    if (angleMercury > 360) angleMercury -= 360;

    angleVenus += 2.0f * speedFactor;
    if (angleVenus > 360) angleVenus -= 360;

    angleEarth += 1.0f * speedFactor;
    if (angleEarth > 360) angleEarth -= 360;

    angleMars += 0.8f * speedFactor;
    if (angleMars > 360) angleMars -= 360;

    angleJupiter += 0.4f * speedFactor;
    if (angleJupiter > 360) angleJupiter -= 360;

    angleSaturn += 0.3f * speedFactor;
    if (angleSaturn > 360) angleSaturn -= 360;

    angleUranus += 0.2f * speedFactor;
    if (angleUranus > 360) angleUranus -= 360;

    angleNeptune += 0.1f * speedFactor;
    if (angleNeptune > 360) angleNeptune -= 360;

    angleMoon += 5.0f * speedFactor; // Угол орбиты спутника, скорость можно настроить
    if (angleMoon > 360) angleMoon -= 360;

    glutPostRedisplay(); // Обновление экрана для анимации
}



void init() {
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_NORMALIZE);
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, 800.0 / 600.0, 1.0, 100.0);
    glMatrixMode(GL_MODELVIEW);
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    glutCreateWindow("Solar System");

    init();
    glutDisplayFunc(display);
    glutIdleFunc(update);

    glutMainLoop();
    return 0;
}
