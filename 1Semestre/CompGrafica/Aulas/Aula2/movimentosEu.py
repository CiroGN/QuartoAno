from OpenGL.GL import * 
from OpenGL.GLUT import * 
from OpenGL.GLU import *
import random
 
# --- Variáveis de Estado (Onde o ponto está e para onde vai) --- 
x_pos = 250.0 
direcao_x = 1.0  # 1 para direita, -1 para esquerda 
y_pos = 250.0 
direcao_y = 1.0  # 1 para cima, -1 para baixo
cores = [ 
    (0.0, 0.0, 0.0), # Preto 
    (1.0, 0.0, 0.0), # Vermelho 
    (0.0, 0.5, 0.0), # Verde 
    (0.0, 0.0, 1.0), # Azul 
    (1.0, 0.5, 0.0)  # Laranja 
]
 
def myInit(): 
    glClearColor(1.0, 1.0, 1.0, 1.0) 
    glColor3f(0, 0, 0) 
    glPointSize(15.0) 
    gluOrtho2D(0, 500, 0, 500) # x_max = 500, y_max = 500, x_min = 0, y_min = 0
 
def animacao(valor): 
    global x_pos, direcao_x, y_pos, direcao_y 
    # Lógica de Movimento 
    x_pos += (direcao_x * 5.0) # Incrementa a posição 
    y_pos += (direcao_y * 5.0) # Incrementa a posição 
 
    # Lógica de Colisão (Se tocar as bordas 0 ou 500, inverte a direção) 
    if x_pos >= 500 or x_pos <= 0:
        direcao_x *= -1 
        glColor3f(random.random(), random.random(), random.random()) # Muda para uma cor aleatória
    if y_pos >= 500 or y_pos <= 0:
        direcao_y *= -1
        glColor3f(random.random(), random.random(), random.random()) # Muda para uma cor aleatória
 
    glutPostRedisplay() # Avisa ao GLUT que a tela mudou e precisa ser redesenhada 
    glutTimerFunc(33, animacao, 0) # Chama esta função novamente em 33ms (~30 FPS) 
 
def display(): 
    glClear(GL_COLOR_BUFFER_BIT) 
    glBegin(GL_POINTS) 
    glVertex2f(x_pos, 250) # O X agora é uma variável! 
    glVertex2f(250, y_pos) # O Y agora é uma variável! 
    glEnd() 
    glFlush() 
 
# --- Setup padrão --- 
glutInit() 
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB) 
glutInitWindowSize(500, 500) 
glutCreateWindow(b'Ponto em Movimento') 
myInit() 
 
glutDisplayFunc(display) 
glutTimerFunc(33, animacao, 0) # Inicia o primeiro ciclo do timer 
glutMainLoop()