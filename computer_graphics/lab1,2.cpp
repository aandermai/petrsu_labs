#include "GLUT/include/GL/glut.h"

// Объявляем переменные для хранения углов вращения
double rotate_x = 0;
double rotate_y = 0;

void display()
{
	// Очистка цвета и глубины
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// Применяют вращения к сцене
	glRotatef(rotate_x, 1.0, 0.0, 0.0);
	glRotatef(rotate_y, 0.0, 1.0, 0.0);

	glBegin(GL_POLYGON);
	glColor3f(1.0, 1.0, 1.0);
	glVertex3f(0.5, -0.5, 0.5);
	glVertex3f(0.5, 0.5, 0.5);
	glVertex3f(-0.5, 0.5, 0.5);
	glVertex3f(-0.5, -0.5, 0.5);
	glEnd();

	glBegin(GL_POLYGON);
	glColor3f(1.0, 0.0, 1.0);
	glVertex3f(0.5, -0.5, -0.5);
	glVertex3f(0.5, 0.5, -0.5);
	glVertex3f(0.5, 0.5, 0.5);
	glVertex3f(0.5, -0.5, 0.5);
	glEnd();

	glBegin(GL_POLYGON);
	glColor3f(0.0, 1.0, 0.0);
	glVertex3f(-0.5, -0.5, 0.5);
	glVertex3f(-0.5, 0.5, 0.5);
	glVertex3f(-0.5, 0.5, -0.5);
	glVertex3f(-0.5, -0.5, -0.5);
	glEnd();

	glBegin(GL_POLYGON);
	glColor3f(0.0, 0.0, 1.0);
	glVertex3f(0.5, 0.5, 0.5);
	glVertex3f(0.5, 0.5, -0.5);
	glVertex3f(-0.5, 0.5, -0.5);
	glVertex3f(-0.5, 0.5, 0.5);
	glEnd();

	glBegin(GL_POLYGON);
	glColor3f(1.0, 1.0, 0.0);
	glVertex3f(0.5, -0.5, -0.5);
	glVertex3f(0.5, -0.5, 0.5);
	glVertex3f(-0.5, -0.5, 0.5);
	glVertex3f(-0.5, -0.5, -0.5);
	glEnd();

	glBegin(GL_POLYGON);
	glColor3f(1.0, 0.0, 0.0);
	glVertex3f(0.5, 0.5, -0.5);
	glVertex3f(0.5, -0.5, -0.5);
	glVertex3f(-0.5, -0.5, -0.5);
	glVertex3f(-0.5, 0.5, -0.5);
	glEnd();

	// Перенос матрицы по осям, чтобы отодвинуть вторую фигуру 
	glTranslatef(-1.5, 0.0, 0.0);

	// Рисуем треугольники по аналогии с квадратами
	glBegin(GL_POLYGON);
	glColor3f(0.5, 0.3, 1.0);
	glVertex3f(0.5, 0.5, 0.5);
	glColor3f(0.9, 0.9, 1.0);
	glVertex3f(-0.5, 0.5, 0.5);
	glColor3f(0.0, 1.0, 0.0);
	glVertex3f(0.5, -0.5, 0.5);
	glEnd();

	glBegin(GL_POLYGON);
	glColor3f(0.5, 0.3, 1.0);
	glVertex3f(0.5, 0.5, 0.5);
	glColor3f(0.9, 0.9, 1.0);
	glVertex3f(-0.5, 0.5, 0.5);
	glColor3f(0.0, 1.0, 0.0);
	glVertex3f(0.5, 0.5, -0.5);
	glEnd();

	glBegin(GL_POLYGON);
	glColor3f(0.5, 0.3, 1.0);
	glVertex3f(0.5, 0.5, 0.5);
	glColor3f(0.9, 0.9, 1.0);
	glVertex3f(0.5, -0.5, 0.5);
	glColor3f(0.0, 1.0, 0.0);
	glVertex3f(0.5, 0.5, -0.5);
	glEnd();

	glBegin(GL_POLYGON);
	glColor3f(0.5, 0.3, 1.0);
	glVertex3f(-0.5, 0.5, 0.5);
	glColor3f(0.9, 0.9, 1.0);
	glVertex3f(0.5, -0.5, 0.5);
	glColor3f(0.0, 1.0, 0.0);
	glVertex3f(0.5, 0.5, -0.5);
	glEnd();

	glFlush(); // Принудительно выполняет команды OpenGL
	glutSwapBuffers(); // Двойная буферизация

	glTranslatef(1.5, 0.0, 0.0);
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

	//  Инициализируем GLUT и обрабатываем пользовательские параметры
	glutInit(&argc, argv);

	// GLUT_DOUBLE (двойная буферизация для плавной анимации), GLUT_RGB (использование цветовой модели RGB), GLUT_DEPTH (использование буфера глубины для корректного отображения объектов при перекрытии)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);

	// Размера и местоположение окна
	glutInitWindowSize(740, 740);
	glutInitWindowPosition(100, 40);

	// настройки цветов
	glClearColor(1.0, 1.0, 1.0, 1.0);

	//Загрузка нулевой матрицы
	glLoadIdentity();

	// Создаем окно
	glutCreateWindow("Cube and Tetraedr");

	//  Активируем тест глубины Z-буферизации
	glEnable(GL_DEPTH_TEST);

	// Выбор матрицы - фигура
	glMatrixMode(GL_PROJECTION);

	// Просмотр матрицы
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

	//Поворот на угол a по осям x,y,z
	glRotatef(330, 1, 1, 1);

	// Объекты не будут уменьшаться в размере при удалении от камеры
	glScalef(0.5, 0.5, 0.5);

	// Функции обратного вызова
	glutDisplayFunc(display);
	glutSpecialFunc(specialKeys);

	// Этот цикл обрабатывает события (нажатия клавиш, изменение размера окна и т.д.) и перерисовку сцены
	glutMainLoop();

	return 0;
}