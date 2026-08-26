import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# --- FUNÃ‡ÃƒO PARA GERAR E DESENHAR O TORUS ---
def desenhar_torus(R, r, num_fatias, num_loops):
    """
    R = Raio maior (distÃ¢ncia do centro ao meio do tubo)
    r = Raio menor (raio do tubo)
    num_fatias = ResoluÃ§Ã£o do tubo (cÃ­rculo interno)
    num_loops = ResoluÃ§Ã£o do anel (cÃ­rculo externo)
    """
    glColor3f(0.3, 0.7, 1.0) # Cor azul clara para as linhas
    
    # Desenha o torus usando malha de quadrilÃ¡teros (GL_QUADS)
    for i in range(num_loops):
        phi1 = 2.0 * math.pi * i / num_loops
        phi2 = 2.0 * math.pi * (i + 1) / num_loops
        
        glBegin(GL_QUAD_STRIP) # Modo eficiente para ligar tiras de quadrados
        for j in range(num_fatias + 1):
            theta = 2.0 * math.pi * j / num_fatias
            
            # Ponto do loop atual (i)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
            
            x1 = (R + r * cos_theta) * math.cos(phi1)
            y1 = (R + r * cos_theta) * math.sin(phi1)
            z1 = r * sin_theta
            
            # Ponto do prÃ³ximo loop (i + 1)
            x2 = (R + r * cos_theta) * math.cos(phi2)
            y2 = (R + r * cos_theta) * math.sin(phi2)
            z2 = r * sin_theta
            
            # Envia os dois vÃ©rtices para formar a tira do quadrilÃ¡tero
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
        glEnd()

def main():
    if not glfw.init(): return
    window = glfw.create_window(800, 600, "Gerador de Torus 3D", None, None)
    if not window:
        glfw.terminate()
        return
        
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    # ConfiguraÃ§Ã£o da CÃ¢mera / ProjeÃ§Ã£o
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    # Define o modo de renderizaÃ§Ã£o como LINHAS (Wireframe) para ver a malha (FILL / LINE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Posiciona e rotaciona a cÃ¢mera para ver o objeto em 3D
        glTranslatef(0.0, 0.0, -6.0)
        glRotatef(glfw.get_time() * 30, 1.0, 0.5, 0.0) # RotaÃ§Ã£o automÃ¡tica

        # Desenha um Torus com Raio Maior = 1.5, Raio Menor = 0.5, 20 fatias e 40 loops
        desenhar_torus(1.5, 0.5, 10, 20)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()