from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# --- Estado do Sistema ---
x_pos, y_pos = 50.0, 50.0   # PosiÃ§Ã£o do Jogador (ComeÃ§a no canto inferior esquerdo)
x_obj, y_obj = 400.0, 400.0 # PosiÃ§Ã£o do Objetivo (Fica no canto superior direito)
velocidade = 20.0
ganhou = False

def myInit():
    # 1. Configura a cor de fundo (Branco)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    # 2. Configura a Lente da CÃ¢mera (ProjeÃ§Ã£o)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 500) # Define a janela de visualizaÃ§Ã£o de 0 a 500
    
    # 3. Volta para o modo de Desenho (Modelview)
    glMatrixMode(GL_MODELVIEW)

def teclas_especiais(tecla, x, y):
    global x_pos, y_pos, ganhou
    
    if ganhou: return 

    if tecla == GLUT_KEY_UP:    y_pos += velocidade
    elif tecla == GLUT_KEY_DOWN:  y_pos -= velocidade
    elif tecla == GLUT_KEY_LEFT:  x_pos -= velocidade
    elif tecla == GLUT_KEY_RIGHT: x_pos += velocidade

    # LÃ³gica de ColisÃ£o
    distancia = math.sqrt((x_pos - x_obj)**2 + (y_pos - y_obj)**2)

    if distancia < 30.0:
        ganhou = True
        print("SISTEMA: OBJETIVO ALCANÃ‡ADO!")

    # ForÃ§a o OpenGL a redesenhar a tela
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Define o tamanho dos pontos para este desenho
    glPointSize(25.0)
    
    # --- DESENHAR OBJETIVO (VERMELHO) ---
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    glVertex2f(x_obj, y_obj)
    glEnd()

    # --- DESENHAR JOGADOR (AZUL OU VERDE) ---
    if ganhou:
        glColor3f(0.0, 0.8, 0.0) # Verde se ganhou
    else:
        glColor3f(0.2, 0.4, 0.8) # Azul enquanto joga
        
    glBegin(GL_POINTS)
    glVertex2f(x_pos, y_pos)
    glEnd()
    
    glFlush()

# --- Setup de ExecuÃ§Ã£o ---
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b'Desafio: Alcance o Objetivo')

myInit() # Chama a configuraÃ§Ã£o de coordenadas

glutDisplayFunc(display)
glutSpecialFunc(teclas_especiais)

print("Use as SETAS do teclado para mover o ponto azul ate o vermelho!")
glutMainLoop()