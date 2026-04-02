import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def desenhar():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(4.0)
    glColor3f(0.0, 0.0, 1.0)

    # círculo no centro com raio 0.5
    raio = 0.5
    lados = 1000

    glBegin(GL_POINTS)
    for i in range(lados):
        angulo = 2 * math.pi * i / lados
        x = math.cos(angulo) * raio
        y = math.sin(angulo) * raio
        glVertex2f(x, y)
    glEnd()

    glFlush()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b"Circulo com glVertex2f")
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(-1, 1, -1, 1)
glutDisplayFunc(desenhar)
glutMainLoop()