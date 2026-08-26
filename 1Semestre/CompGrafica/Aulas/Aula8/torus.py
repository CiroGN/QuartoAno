import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# 1. A FUNÃ‡ÃƒO BÃSICA (Desenha um aro 2D no plano XY)
def desenhar_circunferencia_2d(raio, resolucao=30):  
    glBegin(GL_POINTS)
    for i in range(resolucao):
        angulo = 2.0 * math.pi * i / resolucao
        x = raio * math.cos(angulo)
        y = raio * math.sin(angulo)
        glVertex3f(x, y, 0)
    glEnd()


def desenhar_torus(R, r, rings=40, sides=20):
    # Desenha um tÃ³rus em wireframe como linhas de anel (sides) e circulos ao redor (rings)
    # ParÃ¢metros:
    #  R: raio maior (distÃ¢ncia do centro do toro ao centro do tubo)
    #  r: raio menor (raio do tubo)
    #  rings: quantas divisÃµes ao redor do toro (resolucao do circulo maior)
    #  sides: quantas divisÃµes ao redor do tubo (resolucao do circulo menor)

    # Desenha os pequenos circulos (cross-sections) ao longo dos rings
    for i in range(rings):
        theta = 2.0 * math.pi * i / rings
        glBegin(GL_LINE_LOOP)
        for j in range(sides):
            phi = 2.0 * math.pi * j / sides
            x = (R + r * math.cos(phi)) * math.cos(theta)
            y = r * math.sin(phi)
            z = (R + r * math.cos(phi)) * math.sin(theta)
            glVertex3f(x, y, z)
        glEnd()

    # Desenha linhas conectando os mesmos pontos ao longo dos rings (como longitudes)
    for j in range(sides):
        phi = 2.0 * math.pi * j / sides
        glBegin(GL_LINE_STRIP)
        for i in range(rings + 1):
            theta = 2.0 * math.pi * i / rings
            x = (R + r * math.cos(phi)) * math.cos(theta)
            y = r * math.sin(phi)
            z = (R + r * math.cos(phi)) * math.sin(theta)
            glVertex3f(x, y, z)
        glEnd()

def main():
    if not glfw.init():
        return
        
    window = glfw.create_window(800, 600, "TÃ³rus com CircunferÃªncias (Wireframe)", None, None)
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    # ConfiguraÃ§Ã£o da cÃ¢mara
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    
    # Fundo escuro para destacar as linhas
    glClearColor(0.1, 0.1, 0.15, 1.0) 

    while not glfw.window_should_close(window):
        #  ESC para sair
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Posiciona a cÃ¢mara para ver a figura de cima e de lado
        gluLookAt(0.0, 5.0, 12.0,   0.0, 0.0, 0.0,   0.0, 1.0, 0.0)

        # Roda o TÃ³rus continuamente (eixos X e Y) para vermos o efeito 3D
        tempo = glfw.get_time()
        glRotatef(tempo * 30.0, 1, 1, 0)

        # Desenha o TÃ³rus com uma cor verde nÃ©on (wireframe)
        glColor3f(0.0, 1.0, 0.5)
        glLineWidth(1.2)
        desenhar_torus(3.0, 0.8, rings=64, sides=32)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()