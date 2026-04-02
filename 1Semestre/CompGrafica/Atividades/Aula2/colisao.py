from OpenGL.GL import * 
from OpenGL.GLUT import * 
from OpenGL.GLU import * 
import math # Importação necessária para usar a função de raiz quadrada (sqrt) 
 
# --- Estado do Sistema --- 
x_pos, y_pos = 50.0, 50.0   # Coordenadas atuais do jogador 
x_obj, y_obj = 400.0, 400.0 # Coordenadas fixas do objetivo 
velocidade = 20.0 
ganhou = False 
 
def myInit(): 
    glClearColor(1.0, 1.0, 1.0, 1.0) 
    glPointSize(25.0) 
    gluOrtho2D(0, 500, 0, 500) 
 
def teclas_especiais(tecla, x, y): 
    global x_pos, y_pos, ganhou 
     
    if ganhou: return  
 
    if tecla == GLUT_KEY_UP:    y_pos += velocidade 
    elif tecla == GLUT_KEY_DOWN:  y_pos -= velocidade 
    elif tecla == GLUT_KEY_LEFT:  x_pos -= velocidade 
    elif tecla == GLUT_KEY_RIGHT: x_pos += velocidade 
 
    # --- INÍCIO DA LÓGICA DE COLISÃO --- 
     
    # 1. Aplica o Teorema de Pitágoras: d = sqrt( (x2-x1)^2 + (y2-y1)^2 ) 
    # Esta linha calcula a distância em linha reta entre o centro do jogador e o centro do objetivo. 
    distancia = math.sqrt((x_pos - x_obj)**2 + (y_pos - y_obj)**2) 
 
    # 2. Verifica se a distância calculada é menor que a soma dos raios dos pontos (limiar de colisão). 
    # Como os pontos têm tamanho 25.0, uma distância menor que 30.0 garante que eles visualmente se toquem. 
    if distancia < 30.0:  
        ganhou = True # Altera o estado do sistema para indicar vitória 
        print("SISTEMA: OBJETIVO ALCANÇADO! VOCÊ CHEGOU!") # Feedback no console 
 
    # --- FIM DA LÓGICA DE COLISÃO --- 
 
    glutPostRedisplay() 
 
def display(): 
    glClear(GL_COLOR_BUFFER_BIT) 
     
    # Desenha o Objetivo (Vermelho) 
    glColor3f(1.0, 0.0, 0.0) 
    glBegin(GL_POINTS) 
    glVertex2f(x_obj, y_obj) 
    glEnd() 
 
    # Desenha o Jogador (Azul ou Verde se ganhar) 
    if ganhou: 
        glColor3f(0.0, 0.8, 0.0)  
    else: 
        glColor3f(0.2, 0.4, 0.8) 
         
    glBegin(GL_POINTS) 
    glVertex2f(x_pos, y_pos) 
    glEnd() 
     
    glFlush() 
 
# --- Setup --- 
glutInit() 
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB) 
glutInitWindowSize(500, 500) 
glutCreateWindow(b'Desafio: Alcance o Objetivo') 
myInit() 
glutDisplayFunc(display) 
glutSpecialFunc(teclas_especiais) 
glutMainLoop()