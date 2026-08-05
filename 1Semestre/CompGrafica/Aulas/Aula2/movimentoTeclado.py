from OpenGL.GL import * 
from OpenGL.GLUT import * 
from OpenGL.GLU import * 
 
# --- Estado do Sistema (Posição do Jogador) --- 
x_pos = 250.0 
y_pos = 250.0 
velocidade = 15.0 # Quantos pixels ele pula por clique 
 
def myInit(): 
    glClearColor(1.0, 1.0, 1.0, 1.0) 
    glColor3f(0.2, 0.4, 0.8) # Um azul bonito para o nosso "personagem" 
    glPointSize(25.0)        # Ponto grande para facilitar a visão 
    gluOrtho2D(0, 500, 0, 500) 
 
def teclas_especiais(tecla, x, y): 
    global x_pos, y_pos 
     
    # Lógica de movimentação com as setas 
    if tecla == GLUT_KEY_UP: 
        y_pos += velocidade 
    elif tecla == GLUT_KEY_DOWN: 
        y_pos -= velocidade 
    elif tecla == GLUT_KEY_LEFT: 
        x_pos -= velocidade 
    elif tecla == GLUT_KEY_RIGHT: 
        x_pos += velocidade 
 
    # Tratamento de Bordas (Não deixa o ponto sair da tela) 
    x_pos = max(0, min(500, x_pos)) 
    y_pos = max(0, min(500, y_pos)) 
 
    glutPostRedisplay() # Redesenha a tela após o movimento 
 
def display(): 
    glClear(GL_COLOR_BUFFER_BIT) 
    glBegin(GL_POINTS) 
    glVertex2f(x_pos, y_pos) # Agora x e y são controlados pelo teclado 
    glEnd() 
    glFlush() 
 
# --- Setup --- 
glutInit() 
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB) 
glutInitWindowSize(500, 500) 
glutCreateWindow(b'Controle o Ponto com as Setas') 
myInit() 
 
glutDisplayFunc(display) 
glutSpecialFunc(teclas_especiais) # Registra a função de captura das setas 
glutMainLoop()