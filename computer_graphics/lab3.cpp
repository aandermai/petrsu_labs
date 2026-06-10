#include "GLUT/include/GL/glut.h"
#include "math.h"

double rotate_x = 0;
double rotate_y = 0;

void display()
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// Применяют вращения к сцене
	glRotatef(rotate_x, 1.0, 0.0, 0.0);
	glRotatef(rotate_y, 0.0, 1.0, 0.0);


	glBegin(GL_TRIANGLE_FAN);

	// Цикл для создания круга, а так же его центра
	for (float i = 0;i <= 360;i++)
	{
		if (i == 0) { glColor3f(1.0, 0.0, 1.0);glVertex3f(0.1, 0.1, 1.0); }
		else {
			glColor3f(1.0, 0.7, 0.1);
			glVertex3f(cos(i / (3.14 * 2)), sin(i / (3.14 * 2)), 1.5);
		}
	}
	glEnd();

	// Работаем с фигурой комбинацией треугольников для имитации боков цилиндра
	glBegin(GL_TRIANGLE_STRIP);
	for (float i = 1;i <= 360;i++)
	{
		glColor3f(0.6, 0.1, 0.3);
		glVertex3f(cos(i / (3.14 * 2)), sin(i / (3.14 * 2)), 1.5);
		glColor3f(0.0, 0.2, 1.0);
		glVertex3f(cos(i / (3.14 * 2)), sin(i / (3.14 * 2)), 0.0);
	}

	glEnd();

	// Повторяем первый цикл с другой осью z
	glBegin(GL_TRIANGLE_FAN);
	glColor3f(0.0, 1.0, 0.6);
	for (float i = 0;i <= 360;i++)
	{
		if (i == 0) { glColor3f(0.1, 0.1, 1.0);glVertex3f(0.1, 0.1, 0.0); }
		else {
			glColor3f(0.2, 0.8, 0.1);
			glVertex3f(cos(i / (3.14 * 2)), sin(i / (3.14 * 2)), 0.0);
		}
	}
	glEnd();

	glFlush(); // Принудительно выполняет команды OpenGL
	glutSwapBuffers(); // Двойная буферизация
}

// Функция обработки нажатия стрелок
void specialKeys(int key, int x, int y) {
	switch (key) {

	case GLUT_KEY_UP:    rotate_x += 2; break;
	case GLUT_KEY_DOWN:  rotate_x -= 2; break;
	case GLUT_KEY_LEFT:  rotate_y += 2; break;
	case GLUT_KEY_RIGHT: rotate_y -= 2; break;
	default: break;

	}
	glutPostRedisplay(); // Перерисовка окна
}

int main(int argc, char* argv[]) {

	glutInit(&argc, argv);

	// GLUT_DOUBLE (двойная буферизация для плавной анимации), GLUT_RGB (использование цветовой модели RGB), GLUT_DEPTH (использование буфера глубины для корректного отображения объектов при перекрытии)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);

	// Размера и местоположение окна
	glutInitWindowSize(740, 740);
	glutInitWindowPosition(100, 40);

	// Настройки цветов
	glClearColor(1.0, 1.0, 1.0, 1.0);
	glLoadIdentity();
	glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0);

	// Создаем окно
	glutCreateWindow("Cilindr");

	//  Активируем тест глубины Z-буферизации
	glEnable(GL_DEPTH_TEST);

	// Выбор матрицы - фигура
	glMatrixMode(GL_PROJECTION);
	
	// Просмотр матрицы
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
	
	glMatrixMode(GL_MODELVIEW);

	//Поворот на угол a по осям x,y,z
	glRotatef(270, 0, 1, 1);

	// Объекты не будут уменьшаться в размере при удалении от камеры
	glScalef(0.5, 0.5, 0.5);

	// Функции обратного вызова
	glutDisplayFunc(display);
	glutSpecialFunc(specialKeys);

	// Этот цикл обрабатывает события (нажатия клавиш, изменение размера окна и т.д.) и перерисовку сцены
	glutMainLoop();

	return 0;
}