import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

rx = ry = 0.0
mouse_down = False
last_x = last_y = 0.0

# ------------------------------------------------------------------
# Filtro inicial: GL_LINEAR (bordas suaves)
# Botão direito do mouse alterna para GL_NEAREST (pixelado) e vice-versa
# ------------------------------------------------------------------
filter_mode = GL_LINEAR
filter_name = "GL_LINEAR"
texture_id  = None


def aplicar_filtro(window):
    """Aplica o filtro atual na textura e atualiza o título da janela."""
    global filter_mode, filter_name
    glBindTexture(GL_TEXTURE_2D, texture_id)
    # MIN_FILTER: quando a textura é exibida menor que o original (longe da câmera)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter_mode)
    # MAG_FILTER: quando a textura é ampliada além do original (perto da câmera)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter_mode)
    glfw.set_window_title(window, f'Atividade 5: Filtros  |  Filtro atual: {filter_name}  [Botão Dir = alternar]')
    print(f"[FILTRO] {filter_name}  →  {'Bordas suaves (interpolacao bilinear)' if filter_mode == GL_LINEAR else 'Pixelado (sem interpolacao)'}")


def mouse_button(window, button, action, mods):
    global mouse_down, last_x, last_y, filter_mode, filter_name

    if button == glfw.MOUSE_BUTTON_LEFT:
        mouse_down = action == glfw.PRESS
        if mouse_down:
            last_x, last_y = glfw.get_cursor_pos(window)

    elif button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        # ------------------------------------------------------------------
        # Alterna entre GL_LINEAR e GL_NEAREST em tempo real
        # GL_LINEAR  → suaviza interpolando pixels vizinhos (bilinear)
        # GL_NEAREST → sem interpolação, exibe o pixel mais próximo (pixelado)
        # ------------------------------------------------------------------
        if filter_mode == GL_LINEAR:
            filter_mode = GL_NEAREST
            filter_name = "GL_NEAREST"
        else:
            filter_mode = GL_LINEAR
            filter_name = "GL_LINEAR"
        aplicar_filtro(window)


def cursor_pos(window, xpos, ypos):
    global rx, ry, last_x, last_y
    if mouse_down:
        dx = xpos - last_x
        dy = ypos - last_y
        ry += dx * 0.5
        rx += dy * 0.5
        last_x, last_y = xpos, ypos


def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)
    for verts, norm in [
        # Frente  (+Z)
        ([(0.0,0.0,-0.5,-0.5, 0.5), (1.0,0.0, 0.5,-0.5, 0.5),
          (1.0,1.0, 0.5, 0.5, 0.5), (0.0,1.0,-0.5, 0.5, 0.5)], ( 0, 0, 1)),
        # Trás    (-Z)
        ([(1.0,0.0,-0.5,-0.5,-0.5), (1.0,1.0,-0.5, 0.5,-0.5),
          (0.0,1.0, 0.5, 0.5,-0.5), (0.0,0.0, 0.5,-0.5,-0.5)], ( 0, 0,-1)),
        # Cima    (+Y)
        ([(0.0,1.0,-0.5, 0.5,-0.5), (0.0,0.0,-0.5, 0.5, 0.5),
          (1.0,0.0, 0.5, 0.5, 0.5), (1.0,1.0, 0.5, 0.5,-0.5)], ( 0, 1, 0)),
        # Baixo   (-Y)
        ([(1.0,1.0,-0.5,-0.5,-0.5), (0.0,1.0, 0.5,-0.5,-0.5),
          (0.0,0.0, 0.5,-0.5, 0.5), (1.0,0.0,-0.5,-0.5, 0.5)], ( 0,-1, 0)),
        # Direita (+X)
        ([(0.0,0.0, 0.5,-0.5,-0.5), (0.0,1.0, 0.5, 0.5,-0.5),
          (1.0,1.0, 0.5, 0.5, 0.5), (1.0,0.0, 0.5,-0.5, 0.5)], ( 1, 0, 0)),
        # Esquerda(-X)  ← corrigida: sem UV duplicado
        ([(0.0,0.0,-0.5,-0.5,-0.5), (1.0,0.0,-0.5,-0.5, 0.5),
          (1.0,1.0,-0.5, 0.5, 0.5), (0.0,1.0,-0.5, 0.5,-0.5)], (-1, 0, 0)),
    ]:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()


def main():
    global texture_id

    if not glfw.init():
        return

    window = glfw.create_window(
        800, 600,
        f'Atividade 5: Filtros  |  Filtro atual: {filter_name}  [Botão Dir = alternar]',
        None, None
    )
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)

    init()
    texture_id = criar_textura_checkerboard()

    # Aplica o filtro inicial na textura recém-carregada
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter_mode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter_mode)

    # ------------------------------------------------------------------
    # Explicação didática no terminal
    # ------------------------------------------------------------------
    print("=" * 60)
    print("  Atividade 5 – Alternância de Filtros em Tempo Real")
    print("=" * 60)
    print()
    print("  Filtros de textura controlam como o OpenGL interpola")
    print("  pixels quando a textura é exibida em tamanho diferente")
    print("  do original.")
    print()
    print("  GL_LINEAR  (padrão):")
    print("    Interpola os 4 pixels vizinhos (bilinear filtering).")
    print("    Resultado: bordas suaves, imagem 'borrada' ao ampliar.")
    print("    Uso: texturas fotorrealistas, HUDs, fundos.")
    print()
    print("  GL_NEAREST:")
    print("    Usa o pixel mais proximo sem interpolacao.")
    print("    Resultado: efeito pixelado (estilo pixel art).")
    print("    Uso: jogos retro, Minecraft, sprites 2D.")
    print()
    print("  MIN_FILTER → textura menor que o original (longe)")
    print("  MAG_FILTER → textura maior que o original (perto)")
    print()
    print("  [Botão Direito] Alterna entre GL_LINEAR e GL_NEAREST")
    print("  [Mouse Esq]     Arrasta para rotacionar o cubo")
    print("=" * 60)
    print(f"\n  Filtro inicial: {filter_name}")

    while not glfw.window_should_close(window):
        render()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    main()