#CÃ³digo da PirÃ¢mide
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def calcular_normal(....):
    # fazer os procedimentos do cÃ¡lculo.
    #recebe 3 vÃ©rtices (x,y,z) e retorna a normal "normalizada" (x,y,z)
    
def desenhar_piramide():
    glBegin(GL_TRIANGLES)  
    # --- Face Frontal (Vermelha) ---
    glColor3f(1.0, 0.0, 0.0)
    calcular_normal(...)
    glVertex3f(    ,     ,     )  # Ãpice
    glVertex3f(    ,     ,     )   # Inferior Esquerdo
    glVertex3f(    ,     ,     )   # Inferior Direito

    # --- Face Direita (Verde) ---
    calcular_normal(...)
    glVertex3f(    ,     ,     )  # Ãpice
    glVertex3f(    ,     ,     )   # Inferior Esquerdo
    glVertex3f(    ,     ,     )   # Inferior Direito

    # --- Face Traseira (Azul) ---
    glColor3f(0.0, 0.0, 1.0)
    calcular_normal(...)
    glVertex3f(    ,     ,     )  # Ãpice
    glVertex3f(    ,     ,     )   # Inferior Esquerdo
    glVertex3f(    ,     ,     )   # Inferior Direito

    # --- Face Esquerda (Amarela) ---
    glColor3f(1.0, 1.0, 0.0)
    calcular_normal(...)
    glVertex3f(    ,     ,     )  # Ãpice
    glVertex3f(    ,     ,     )   # Inferior Esquerdo
    glVertex3f(    ,     ,     )   # Inferior Direito
    
    # --- Base Quadrada (Magenta) - Dividida em 2 triÃ¢ngulos ---
    glColor3f(1.0, 0.0, 1.0)
    # Primeiro TriÃ¢ngulo da Base
    calcular_normal(...)
    glVertex3f(    ,     ,     )  
    glVertex3f(    ,     ,     )  
    glVertex3f(    ,     ,     )
    
    # Segundo TriÃ¢ngulo da Base
    glVertex3f(    ,     ,     )  
    glVertex3f(    ,     ,     )  
    glVertex3f(    ,     ,     )
    

    glEnd()

def desenhar_cubo():
    # CÃ³digo para desenhar o cubo

def main():
    glfw.init()
    janela = glfw.create_window(800, 600, "PirÃ¢mide Ãšnica com TriÃ¢ngulos", None, None)
    glfw.make_context_current(janela)
    glEnable(GL_DEPTH_TEST) # Habilita o teste de profundidade para o 3D

    # ConfiguraÃ§Ã£o da ProjeÃ§Ã£o
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(janela):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        #Posiciona e rotaciona a pirÃ¢mide para visualizaÃ§Ã£o
        glTranslatef(0.0, 0.0, -6.0) # Afasta da tela (zoom in), se necessÃ¡rio
        glRotatef(glfw.get_time() * 50, 0, 1, 0) # RotaÃ§Ã£o automÃ¡tica no eixo Y
        glRotatef(20, 1, 0, 0)  # InclinaÃ§Ã£o fixa para ver o topo e a base
        
        desenhar_piramide()
        desenhar_quadrado()
        glfw.swap_buffers(janela)
        glfw.poll_events()
    glfw.terminate()
main()