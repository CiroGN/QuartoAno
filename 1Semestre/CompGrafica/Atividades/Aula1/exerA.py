from OpenGL.GL import * 
from OpenGL.GLUT import * 
from OpenGL.GLU import * 
def desenhar(): 
    glClear(GL_COLOR_BUFFER_BIT) # Limpa a tela (apaga o frame anterior) 
    glPointSize(10.0)            # Define o tamanho do ponto 
    glBegin(GL_POINTS)           # Inicia o modo de desenho de pontos 
    i = -0.5
    j = 0.5
    while i < 0.5:
        glColor3f(0.8, 1.0, 0.0)     # Escolhe a cor Vermelha (R,G,B) 
        glVertex2f(i, j)
        i += 0.01
    while j > -0.5:
        glColor3f(0.3, 0.5, 0.4)     # Escolhe a cor Vermelha (R,G,B) 
        glVertex2f(i, j)
        j -= 0.01
    while i > -0.5:
        glColor3f(0.8, 1.0, 1.0)     # Escolhe a cor Vermelha (R,G,B) 
        glVertex2f(i, -0.5)
        i -= 0.01    
    while j < 0.5:
        glColor3f(1.0, 0.0, 0.0)     # Escolhe a cor Vermelha (R,G,B) 
        glVertex2f(i, j)
        j += 0.01  
    
    
    glColor3f(1.0, 0.0, 0.0)     # Escolhe a cor Vermelha (R,G,B) 
    glVertex2f(0.0, 0.0)         # Posiciona o ponto no centro (0,0) 
    glEnd()                      # Finaliza o desenho 
    glFlush()                    # Envia os dados para a placa de vídeo 
# Configuração da Janela 
glutInit() 
glutInitWindowSize(500, 500) 
glutCreateWindow(b"Exercicio A - Quadrado") 
glutDisplayFunc(desenhar)        # Registro da função de desenho 
glutMainLoop()                   # Inicia o programa 