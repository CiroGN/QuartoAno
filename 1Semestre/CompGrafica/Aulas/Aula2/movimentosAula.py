from OpenGL.GL import * 
from OpenGL.GLUT import * 
from OpenGL.GLU import *
import random # Vamos usar para iniciar com uma cor aleatória 
 
# --- Estado do Sistema --- 
x_pos = 250.0 
direcao = 1.0 
indice_cor = 0 
 
# --- Lista de Cores (Paleta RGB) --- 
# Cada item é uma tupla (R, G, B) 
cores = [ 
    (0.0, 0.0, 0.0), # Preto 
    (1.0, 0.0, 0.0), # Vermelho 
    (0.0, 0.5, 0.0), # Verde 
    (0.0, 0.0, 1.0), # Azul 
    (1.0, 0.5, 0.0)  # Laranja 
] 
 
def myInit(): 
    glClearColor(1.0, 1.0, 1.0, 1.0) 
    glPointSize(20.0) # Aumentei para destacar a cor 
    gluOrtho2D(0, 500, 0, 500) 
 
def animacao(valor): 
    global x_pos, direcao, indice_cor 
     
    x_pos += (direcao * 7.0) 
     
    # Lógica de Colisão + Troca de Cor 
    if x_pos >= 500 or x_pos <= 0: 
        direcao *= -1 
        # Lógica de Índice Circular: vai de 0 a 4 e volta para 0 
        indice_cor = (indice_cor + 1) % len(cores) 
         
    glutPostRedisplay() 
    glutTimerFunc(33, animacao, 0) 
 
def display(): 
    glClear(GL_COLOR_BUFFER_BIT) 
     
    # Define a cor atual baseada no índice da nossa lista 
    r, g, b = cores[indice_cor] 
    glColor3f(r, g, b) 
     
    glBegin(GL_POINTS) 
    glVertex2f(x_pos, 250) 
    glEnd() 
    glFlush() 
 
# --- Setup --- 
glutInit() 
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB) 
glutInitWindowSize(500, 500) 
glutCreateWindow(b'Ponto Colorido Rebatendo') 
myInit() 
glutDisplayFunc(display) 
glutTimerFunc(33, animacao, 0) 
glutMainLoop()