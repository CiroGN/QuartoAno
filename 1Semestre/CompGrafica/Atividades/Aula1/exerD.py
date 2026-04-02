import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def desenhar():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # preenchimento do coração em vermelho
    glColor3f(1.0, 0.5, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.0, 0.03)  # centro para o fan

    n = 300
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        x = 0.16 * math.sin(t) ** 3
        y = (0.13 * math.cos(t) - 0.05 * math.cos(2 * t)
             - 0.02 * math.cos(3 * t) - 0.01 * math.cos(4 * t))
        glVertex2f(x, y)

    glEnd()

    # contorno com linha para reforçar a borda
    glLineWidth(2.0)
    glColor3f(0.8, 0.5, 0.0)
    glBegin(GL_LINE_LOOP)
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        x = 0.16 * math.sin(t) ** 3
        y = (0.13 * math.cos(t) - 0.05 * math.cos(2 * t)
             - 0.02 * math.cos(3 * t) - 0.01 * math.cos(4 * t))
        glVertex2f(x, y)
    glEnd()

    glFlush()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b"Coracao Alaranjado")
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(-1, 1, -1, 1)
glutDisplayFunc(desenhar)
glutMainLoop()