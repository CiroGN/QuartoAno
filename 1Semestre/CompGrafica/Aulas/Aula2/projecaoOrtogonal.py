from OpenGL.GL import * 
from OpenGL.GLUT import * 
from OpenGL.GLU import * 

def desenhar(): 
    glClear(GL_COLOR_BUFFER_BIT) # Limpa a tela (apaga o frame anterior) 
    glLineWidth(3.0)  # Largura da linha 
    glBegin(GL_LINE_LOOP)  # Inicia o modo de desenho como um loop de linhas 
    glColor3f(1.0, 0.0, 0.0)     # Escolhe a cor Vermelha (R,G,B) 
    glVertex2f(0.0, 0.0)         # Posiciona o ponto no centro (0,0) 
    glVertex2f(250, 0.0) 
    glVertex2f(250, 250) 
    glVertex2f(0.0, 250) 
    glEnd()                      # Finaliza o desenho 
    glFlush()                    # Envia os dados para a placa de vídeo 

# Configuração da Janela 
glutInit() 
# glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB) 
glutInitWindowSize(500, 500) #Tamanho da tela em pixels 
glutCreateWindow(b"Aula 2 - Linhas") 
# gluOrtho2D(0.0, 1.0, 0.0, 1.0)  # Define o sistema de coordenadas 
gluOrtho2D(0, 500, 0, 500) # modo não normalizado 
glutDisplayFunc(desenhar)         
glutMainLoop()                   # Inicia o programa