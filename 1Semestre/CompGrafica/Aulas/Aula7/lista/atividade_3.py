import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

rx = ry = 0.0
mouse_down = False
last_x = last_y = 0.0


def mouse_button(window, button, action, mods):
    global mouse_down, last_x, last_y
    if button == glfw.MOUSE_BUTTON_LEFT:
        mouse_down = action == glfw.PRESS
        if mouse_down:
            last_x, last_y = glfw.get_cursor_pos(window)


def cursor_pos(window, xpos, ypos):
    global rx, ry, last_x, last_y
    if mouse_down:
        dx = xpos - last_x
        dy = ypos - last_y
        rx += dy * 0.5
        ry += dx * 0.5
        last_x, last_y = xpos, ypos


def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)


def render(texture_id):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    # ------------------------------------------------------------------
    # GL_CLAMP_TO_EDGE:
    # As coordenadas UV vão de 1.0 a 3.0 (além do limite normal de 1.0).
    # Com GL_CLAMP_TO_EDGE, o OpenGL pega o último pixel da borda da
    # imagem e o "estica" para cobrir o restante do polígono.
    # Efeito visual: a textura aparece uma vez e, ao redor dela, surgem
    # listras sólidas com a cor da borda da imagem.
    # ------------------------------------------------------------------
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)  # eixo horizontal
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)  # eixo vertical

    # ------------------------------------------------------------------
    # Cubo com UVs de 1.0 a 3.0 — força o comportamento de wrap
    # ------------------------------------------------------------------
    glBegin(GL_QUADS)
    for verts, norm in [
        # Frente  (+Z)
        ([(1.0, 1.0, -0.5, -0.5,  0.5), (3.0, 1.0,  0.5, -0.5,  0.5),
          (3.0, 3.0,  0.5,  0.5,  0.5), (1.0, 3.0, -0.5,  0.5,  0.5)], (0,  0,  1)),
        # Trás    (-Z)
        ([(3.0, 1.0, -0.5, -0.5, -0.5), (3.0, 3.0, -0.5,  0.5, -0.5),
          (1.0, 3.0,  0.5,  0.5, -0.5), (1.0, 1.0,  0.5, -0.5, -0.5)], (0,  0, -1)),
        # Cima    (+Y)
        ([(1.0, 3.0, -0.5,  0.5, -0.5), (1.0, 1.0, -0.5,  0.5,  0.5),
          (3.0, 1.0,  0.5,  0.5,  0.5), (3.0, 3.0,  0.5,  0.5, -0.5)], (0,  1,  0)),
        # Baixo   (-Y)
        ([(3.0, 3.0, -0.5, -0.5, -0.5), (1.0, 3.0,  0.5, -0.5, -0.5),
          (1.0, 1.0,  0.5, -0.5,  0.5), (3.0, 1.0, -0.5, -0.5,  0.5)], (0, -1,  0)),
        # Direita (+X)
        ([(1.0, 1.0,  0.5, -0.5, -0.5), (1.0, 3.0,  0.5,  0.5, -0.5),
          (3.0, 3.0,  0.5,  0.5,  0.5), (3.0, 1.0,  0.5, -0.5,  0.5)], (1,  0,  0)),
        # Esquerda(-X)  ← corrigida: sem vértice UV duplicado
        ([(1.0, 1.0, -0.5, -0.5, -0.5), (3.0, 1.0, -0.5, -0.5,  0.5),
          (3.0, 3.0, -0.5,  0.5,  0.5), (1.0, 3.0, -0.5,  0.5, -0.5)], (-1, 0,  0)),
    ]:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(
        800, 600,
        'Atividade 3: GL_CLAMP_TO_EDGE – Borda Esticada',
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

    # ------------------------------------------------------------------
    # Explicação didática no terminal (conforme conceito do PDF)
    # ------------------------------------------------------------------
    print("=" * 60)
    print("  Atividade 3 – GL_CLAMP_TO_EDGE (Borda Esticada)")
    print("=" * 60)
    print()
    print("  Modo de wrap ativo: GL_CLAMP_TO_EDGE")
    print()
    print("  As coordenadas UV vao de 1.0 a 3.0 (alem do limite 1.0).")
    print("  Com CLAMP_TO_EDGE, o OpenGL nao repete a imagem.")
    print("  Em vez disso, ele pega o ultimo pixel da borda e o")
    print("  'estica' infinitamente para cobrir o resto do poligono.")
    print()
    print("  Efeito visual esperado:")
    print("    - A textura aparece UMA vez no centro da face.")
    print("    - As bordas da face exibem listras solidas de cor,")
    print("      'puxadas' do ultimo pixel da imagem.")
    print()
    print("  Caso de uso real (por que isso importa?):")
    print("    Texturas PNG com fundo transparente e filtro GL_LINEAR")
    print("    podem gerar uma borda preta/colorida ao redor do sprite")
    print("    (Texture Bleeding). GL_CLAMP_TO_EDGE elimina esse artefato")
    print("    duplicando o pixel transparente da borda, em vez de")
    print("    'puxar' pixels do lado oposto da imagem.")
    print()
    print("  [Mouse] Arraste para rotacionar o cubo.")
    print("=" * 60)

    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    main()