from OpenGL.GL import * 
from OpenGL.GLUT import * 
from OpenGL.GLU import * 
def desenhar(): 
    glClear(GL_COLOR_BUFFER_BIT) # Limpa a tela (apaga o frame anterior) 
    glPointSize(10.0)            # Define o tamanho do ponto 
    glBegin(GL_POINTS)           # Inicia o modo de desenho de pontos 
    glColor3f(1.0, 0.0, 0.0)     # Escolhe a cor Vermelha (R,G,B) 
    glVertex2f(0.0, 0.0)         # Posiciona o ponto no centro (0,0) 
    glEnd()                      # Finaliza o desenho 
    glFlush()                    # Envia os dados para a placa de vídeo 
# Configuração da Janela 
glutInit() 
glutInitWindowSize(500, 500) 
glutCreateWindow(b"Aula 01 - Primeiro Ponto") 
glutDisplayFunc(desenhar)        # Registro da função de desenho 
glutMainLoop()                   # Inicia o programa 