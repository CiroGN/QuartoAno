import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# --- VariÃ¡veis Globais de NavegaÃ§Ã£o ---
rot_x = 20.0  # RotaÃ§Ã£o vertical (Cima/Baixo)
rot_y = 45.0  # RotaÃ§Ã£o horizontal (Ao redor)
distancia = -10.0 # DistÃ¢ncia da cÃ¢mera (Zoom)

def tratar_teclado(window, key, scancode, action, mods):
    global rot_x, rot_y, distancia
    passo = 2.0 # Velocidade da rotaÃ§Ã£o
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        # Setas Esquerda/Direita: Gira ao redor da casa
        if key == glfw.KEY_LEFT: rot_y -= passo
        if key == glfw.KEY_RIGHT: rot_y += passo
        
        # Setas Cima/Baixo: Sobe ou desce a visÃ£o
        if key == glfw.KEY_UP: rot_x -= passo
        if key == glfw.KEY_DOWN: rot_x += passo
        
        # Teclas W/S: Zoom (Para frente e para trÃ¡s)
        if key == glfw.KEY_W: distancia += 0.5
        if key == glfw.KEY_S: distancia -= 0.5

def desenhar_cubo(largura, altura, profundidade):
    glBegin(GL_QUADS)
    # Face Frontal (Bege)
    glColor3f(0.8, 0.7, 0.5)
    glVertex3f(-largura, 0, profundidade); glVertex3f(largura, 0, profundidade)
    glVertex3f(largura, altura, profundidade); glVertex3f(-largura, altura, profundidade)
    # Face Traseira
    glVertex3f(-largura, 0, -profundidade); glVertex3f(-largura, altura, -profundidade)
    glVertex3f(largura, altura, -profundidade); glVertex3f(largura, 0, -profundidade)
    # Lateral Direita
    glColor3f(0.7, 0.6, 0.4)
    glVertex3f(largura, 0, profundidade); glVertex3f(largura, 0, -profundidade)
    glVertex3f(largura, altura, -profundidade); glVertex3f(largura, altura, profundidade)
    # Lateral Esquerda
    glVertex3f(-largura, 0, profundidade); glVertex3f(-largura, altura, profundidade)
    glVertex3f(-largura, altura, -profundidade); glVertex3f(-largura, 0, -profundidade)
    glEnd()

    # Porta
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.2, 0.0)
    glVertex3f(-0.3, 0, profundidade + 0.01)
    glVertex3f(0.3, 0, profundidade + 0.01)
    glVertex3f(0.3, 1.2, profundidade + 0.01)
    glVertex3f(-0.3, 1.2, profundidade + 0.01)
    glEnd()

def desenhar_telhado(largura, altura_base, profundidade):
    altura_telhado = altura_base + 1.5
    glBegin(GL_TRIANGLES)
    glColor3f(0.6, 0.2, 0.2)
    # Frontal
    glVertex3f(-largura - 0.2, altura_base, profundidade + 0.2)
    glVertex3f(largura + 0.2, altura_base, profundidade + 0.2)
    glVertex3f(0, altura_telhado, 0)
    # Traseiro
    glVertex3f(-largura - 0.2, altura_base, -profundidade - 0.2)
    glVertex3f(0, altura_telhado, 0)
    glVertex3f(largura + 0.2, altura_base, -profundidade - 0.2)
    glEnd()
    
    glBegin(GL_QUADS) # Laterais do telhado
    glColor3f(0.5, 0.1, 0.1)
    glVertex3f(largura + 0.2, altura_base, profundidade + 0.2)
    glVertex3f(largura + 0.2, altura_base, -profundidade - 0.2)
    glVertex3f(0, altura_telhado, 0); glVertex3f(0, altura_telhado, 0)
    glVertex3f(-largura - 0.2, altura_base, profundidade + 0.2)
    glVertex3f(0, altura_telhado, 0); glVertex3f(0, altura_telhado, 0)
    glVertex3f(-largura - 0.2, altura_base, -profundidade - 0.2)
    glEnd()

def main():
    if not glfw.init(): return
    janela = glfw.create_window(800, 600, "NavegaÃ§Ã£o na Casa 3D", None, None)
    glfw.make_context_current(janela)
    glfw.set_key_callback(janela, tratar_teclado)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(janela):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # --- APLICAÃ‡ÃƒO DA NAVEGAÃ‡ÃƒO ---
        glTranslatef(0, -1, distancia) # Afasta/Aproxima a cÃ¢mera
        glRotatef(rot_x, 1, 0, 0)      # Gira em torno do eixo X (Vertical)
        glRotatef(rot_y, 0, 1, 0)      # Gira em torno do eixo Y (Horizontal)

        desenhar_cubo(2, 2, 2)
        desenhar_telhado(2, 2, 2)

        glfw.swap_buffers(janela)
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()