from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# --- Estado do Sistema ---
x_pos, y_pos = 50.0, 50.0
x_obj, y_obj = 400.0, 400.0
velocidade = 20.0
ganhou = False

def myInit():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 500)
    glMatrixMode(GL_MODELVIEW)

def verificar_colisao():
    """FunÃ§Ã£o centralizada para checar se o jogador tocou o objetivo."""
    global ganhou
    distancia = math.sqrt((x_pos - x_obj)**2 + (y_pos - y_obj)**2)
    if distancia < 30.0:
        ganhou = True
        print("SISTEMA: OBJETIVO ALCANÃ‡ADO!")

def teclado_comum(tecla, x, y):
    """Trata as teclas WASD (letras)."""
    global x_pos, y_pos
    if ganhou: return

    # O .lower() serve para aceitar tanto 'W' quanto 'w'
    tecla = tecla.lower()

    if tecla == b'w':   y_pos += velocidade
    elif tecla == b's': y_pos -= velocidade
    elif tecla == b'a': x_pos -= velocidade
    elif tecla == b'd': x_pos += velocidade
    
    # Tecla ESC para sair
    if tecla == chr(27).encode() : # ou    b'\x1b' em hexadecimal  #tecla esc

        glutLeaveMainLoop()  # finaliza a execuÃ§Ã£o

    verificar_colisao()
    glutPostRedisplay()

def teclado_especial(tecla, x, y):
    """Trata as Setas do Teclado."""
    global x_pos, y_pos
    if ganhou: return

    if tecla == GLUT_KEY_UP:    y_pos += velocidade
    elif tecla == GLUT_KEY_DOWN:  y_pos -= velocidade
    elif tecla == GLUT_KEY_LEFT:  x_pos -= velocidade
    elif tecla == GLUT_KEY_RIGHT: x_pos += velocidade

    verificar_colisao()
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(25.0)
    
    # Objetivo
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    glVertex2f(x_obj, y_obj)
    glEnd()

    # Jogador
    if ganhou: glColor3f(0.0, 0.8, 0.0)
    else: glColor3f(0.2, 0.4, 0.8)
        
    glBegin(GL_POINTS)
    glVertex2f(x_pos, y_pos)
    glEnd()
    
    glFlush()

# --- Setup Final ---
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b'Desafio: Setas ou WASD')

myInit()

glutDisplayFunc(display)
# REGISTRO DAS DUAS FUNÃ‡Ã•ES DE TECLADO:
glutKeyboardFunc(teclado_comum)   # Para letras (WASD)
glutSpecialFunc(teclado_especial) # Para setas

print("Controles Ativos: SETAS ou WASD. Pressione ESC para sair.")
glutMainLoop()