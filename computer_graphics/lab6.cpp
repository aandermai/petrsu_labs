#include <stdlib.h>
#include "GLUT/include/GL/glut.h"
#define STB_IMAGE_IMPLEMENTATION
#include "./stb_image.h"
#include <cstdlib>
#include <math.h>

float light[] = { 1, 1, 1, 0 };
GLuint topTexture, bottomTexture, flankTexture;

float angleX = 0.0f; // Угол для вращения по оси X
float angleY = 0.0f; // Угол для вращения по оси Y

GLuint loadTexture(const char* filename) {
    int width, height, channels;
    unsigned char* data = stbi_load(filename, &width, &height, &channels, 0);
    if (!data) {
        printf("Error loading texture %s\n", filename);
        return 0;
    }

    GLuint texture;
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);
    glTexImage2D(GL_TEXTURE_2D, 0, channels == 4 ? GL_RGBA : GL_RGB, width, height, 0,
        channels == 4 ? GL_RGBA : GL_RGB, GL_UNSIGNED_BYTE, data);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    stbi_image_free(data);
    return texture;
}

void initTextures() {
    topTexture = loadTexture("./images/top_1.png");
    bottomTexture = loadTexture("./images/bottom_1.png");
    flankTexture = loadTexture("./images/flank_1.jpg");
}

void drawCanFlank(float radius, float height) {
    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, flankTexture);
    glBegin(GL_QUAD_STRIP);
    for (int i = 0; i <= 360; i += 10) {
        float angle = i * 3.14159 / 180;
        float x = radius * cos(angle);
        float z = radius * sin(angle);

        glNormal3f(cos(angle), 0, sin(angle));

        glTexCoord2f(1.0f - (i / 360.0f), 0);
        glVertex3f(x, -height / 2, z);
        glTexCoord2f(1.0f - (i / 360.0f), 1);
        glVertex3f(x, height / 2, z);
    }
    glEnd();
    glDisable(GL_TEXTURE_2D);
}

void drawCanTopBottom(float radius, GLuint textureID, float y) {
    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, textureID);
    glBegin(GL_TRIANGLE_FAN);
    glNormal3f(0, y > 0 ? 1 : -1, 0);
    glTexCoord2f(0.5, 0.5);
    glVertex3f(0, y, 0);
    for (int i = 0; i <= 360; i += 10) {
        float angle = i * 3.14159 / 180;
        float x = radius * cos(angle);
        float z = radius * sin(angle);
        glTexCoord2f(0.5 + 0.5 * cos(angle), 0.5 + 0.5 * sin(angle));
        glVertex3f(x, y, z);
    }
    glEnd();
    glDisable(GL_TEXTURE_2D);
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    gluLookAt(0.0, 2.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);

    GLfloat lightAmbient[] = { 0.2f, 0.2f, 0.2f, 1.0f };
    GLfloat lightDiffuse[] = { 0.8f, 0.8f, 0.8f, 1.0f };
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse);
    glLightfv(GL_LIGHT0, GL_POSITION, light);

    // Поворот банки: вращение по осям X и Y
    glRotatef(angleX, 1.0f, 0.0f, 0.0f);
    glRotatef(angleY, 0.0f, 1.0f, 0.0f);

    float radius = 1.0;
    float height = 2.0;
    drawCanFlank(radius, height);
    drawCanTopBottom(radius, topTexture, height / 2);
    drawCanTopBottom(radius, bottomTexture, -height / 2);

    glutSwapBuffers();
}

void init() {
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_TEXTURE_2D);
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);
    glEnable(GL_NORMALIZE);

    glClearColor(0.1f, 0.1f, 0.1f, 1.0f);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, 800.0 / 600.0, 1.0, 100.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    initTextures();
}

// Обработчик нажатия клавиш стрелок
void handleSpecialKeypress(int key, int x, int y) {
    const float rotationSpeed = 5.0f;
    switch (key) {
    case GLUT_KEY_UP:
        angleX -= rotationSpeed;
        break;
    case GLUT_KEY_DOWN:
        angleX += rotationSpeed;
        break;
    case GLUT_KEY_LEFT:
        angleY -= rotationSpeed;
        break;
    case GLUT_KEY_RIGHT:
        angleY += rotationSpeed;
        break;
    }
    glutPostRedisplay(); // Запрашиваем перерисовку
}

void handleKeypress(unsigned char key, int x, int y) {
    if (key == 27) {
        std::exit(0);
    }
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    glutCreateWindow("Банка");

    init();

    glutDisplayFunc(display);
    glutSpecialFunc(handleSpecialKeypress); // Добавляем обработчик специальных клавиш (стрелок)
    glutKeyboardFunc(handleKeypress);
    glutMainLoop();
    return 0;
}
