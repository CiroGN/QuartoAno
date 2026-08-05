import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_atlas

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


# ------------------------------------------------------------------
# Layout do Texture Atlas (grade 3 colunas × 2 linhas)
#
#   +-------+-------+-------+
#   | Face1 | Face2 | Face3 |  linha 0  (V: 0.0 → 0.5)
#   +-------+-------+-------+
#   | Face4 | Face5 | Face6 |  linha 1  (V: 0.5 → 1.0)
#   +-------+-------+-------+
#    col 0   col 1   col 2
#   U: 0.0  0.33   0.66   1.0
#
# Cada célula ocupa 1/3 da largura (≈0.333) e 1/2 da altura (0.5).
# Faces do dado atribuídas:
#   Frente  (+Z) → Face 1  (col 0, linha 0)
#   Trás    (-Z) → Face 2  (col 1, linha 0)
#   Cima    (+Y) → Face 3  (col 2, linha 0)
#   Baixo   (-Y) → Face 4  (col 0, linha 1)
#   Direita (+X) → Face 5  (col 1, linha 1)
#   Esquerda(-X) → Face 6  (col 2, linha 1)
# ------------------------------------------------------------------

# Atalhos para os cantos UV de cada célula do atlas
# uv_cell(col, row) → (u0, u1, v0, v1)
def uv_cell(col, row):
    u0 = col / 3.0
    u1 = (col + 1) / 3.0
    v0 = row / 2.0
    v1 = (row + 1) / 2.0
    return u0, u1, v0, v1


def quad_uvs(col, row):
    """Retorna os 4 pares UV no sentido anti-horário para um quad."""
    u0, u1, v0, v1 = uv_cell(col, row)
    # Ordem: inferior-esquerdo, inferior-direito, superior-direito, superior-esquerdo
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


def render(texture_id):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    # ------------------------------------------------------------------
    # GL_CLAMP_TO_EDGE é OBRIGATÓRIO no atlas!
    # Sem ele, o OpenGL vaza pixels de uma célula para a célula vizinha
    # (Texture Bleeding) ao interpolar as bordas — borrando os números
    # do dado nas arestas.
    # ------------------------------------------------------------------
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    # Vértices 3D de cada face do cubo (x, y, z) por quad
    # Ordem dos vértices espelha a ordem UV: inf-esq, inf-dir, sup-dir, sup-esq
    faces = [
        # (col_atlas, lin_atlas, [v0, v1, v2, v3],        normal)
        (0, 0, [(-0.5,-0.5, 0.5),( 0.5,-0.5, 0.5),( 0.5, 0.5, 0.5),(-0.5, 0.5, 0.5)], ( 0, 0, 1)),  # Frente
        (1, 0, [(-0.5,-0.5,-0.5),(-0.5, 0.5,-0.5),( 0.5, 0.5,-0.5),( 0.5,-0.5,-0.5)], ( 0, 0,-1)),  # Trás
        (2, 0, [(-0.5, 0.5,-0.5),(-0.5, 0.5, 0.5),( 0.5, 0.5, 0.5),( 0.5, 0.5,-0.5)], ( 0, 1, 0)),  # Cima
        (0, 1, [(-0.5,-0.5,-0.5),( 0.5,-0.5,-0.5),( 0.5,-0.5, 0.5),(-0.5,-0.5, 0.5)], ( 0,-1, 0)),  # Baixo
        (1, 1, [( 0.5,-0.5,-0.5),( 0.5, 0.5,-0.5),( 0.5, 0.5, 0.5),( 0.5,-0.5, 0.5)], ( 1, 0, 0)),  # Direita
        (2, 1, [(-0.5,-0.5,-0.5),(-0.5,-0.5, 0.5),(-0.5, 0.5, 0.5),(-0.5, 0.5,-0.5)], (-1, 0, 0)),  # Esquerda
    ]

    glBegin(GL_QUADS)
    for col, row, verts, norm in faces:
        uvs = quad_uvs(col, row)
        glNormal3f(*norm)
        for (u, v), (x, y, z) in zip(uvs, verts):
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(
        800, 600,
        'Atividade 4: Texture Atlas – Dado de 6 Faces',
        None, None
    )
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)

    init()
    texture_id = criar_textura_atlas()

    # ------------------------------------------------------------------
    # Explicação didática no terminal
    # ------------------------------------------------------------------
    print("=" * 60)
    print("  Atividade 4 – Texture Atlas (Dado de 6 Faces)")
    print("=" * 60)
    print()
    print("  Conceito: Otimizacao de Memoria (Texture Atlas)")
    print()
    print("  Em vez de carregar 6 texturas separadas (uma por face),")
    print("  usamos UMA unica imagem dividida em uma grade 3x2.")
    print("  Cada face do cubo aponta para uma regiao diferente")
    print("  dessa imagem usando coordenadas UV calculadas.")
    print()
    print("  Layout do Atlas (3 colunas x 2 linhas):")
    print("  +--------+--------+--------+")
    print("  | Face 1 | Face 2 | Face 3 |  <- linha 0 (V: 0.0 a 0.5)")
    print("  +--------+--------+--------+")
    print("  | Face 4 | Face 5 | Face 6 |  <- linha 1 (V: 0.5 a 1.0)")
    print("  +--------+--------+--------+")
    print("    col 0    col 1    col 2")
    print()
    print("  Mapeamento das faces do cubo:")
    print("    Frente  (+Z) → Face 1  (col 0, linha 0)")
    print("    Tras    (-Z) → Face 2  (col 1, linha 0)")
    print("    Cima    (+Y) → Face 3  (col 2, linha 0)")
    print("    Baixo   (-Y) → Face 4  (col 0, linha 1)")
    print("    Direita (+X) → Face 5  (col 1, linha 1)")
    print("    Esquerda(-X) → Face 6  (col 2, linha 1)")
    print()
    print("  GL_CLAMP_TO_EDGE ativo → evita Texture Bleeding")
    print("  entre celulas vizinhas do atlas.")
    print()
    print("  [Mouse] Arraste para rotacionar o dado.")
    print("=" * 60)

    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    main()