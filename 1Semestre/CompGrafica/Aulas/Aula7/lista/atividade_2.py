import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

rx = ry = 0.0
mouse_down = False
last_x = last_y = 0.0

# -------------------------------------------------------
# Modos de wrap disponíveis para alternância (ESPAÇO)
# -------------------------------------------------------
wrap_modes = [GL_REPEAT, GL_MIRRORED_REPEAT, GL_CLAMP_TO_EDGE]
wrap_names = ["GL_REPEAT", "GL_MIRRORED_REPEAT", "GL_CLAMP_TO_EDGE"]
wrap_desc  = [
    "Repete a textura normalmente (efeito mosaico)",
    "Repete espelhando a cada tile (sem emendas obvias)",
    "Estica a cor da borda ate o infinito",
]
current_mode = 0   # índice atual


def key_callback(window, key, scancode, action, mods):
    """Tecla ESPAÇO avança para o próximo modo de wrap."""
    global current_mode
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        current_mode = (current_mode + 1) % len(wrap_modes)
        nome = wrap_names[current_mode]
        desc = wrap_desc[current_mode]
        print(f"[WRAP MODE] {nome}  →  {desc}")
        glfw.set_window_title(
            window,
            f"Atividade 2: Texture Wrapping  |  [{current_mode+1}/{len(wrap_modes)}] {nome}"
        )


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

    # -------------------------------------------------------
    # Aplica o modo de wrap atual nos dois eixos (S e T)
    # -------------------------------------------------------
    modo = wrap_modes[current_mode]
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, modo)  # eixo horizontal (U)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, modo)  # eixo vertical   (V)

    # -------------------------------------------------------
    # Cubo com UVs de 1.0 a 3.0  →  3 repetições por face
    # (0.0–1.0 = intervalo normal; ir até 3.0 força o wrap)
    # -------------------------------------------------------
    glBegin(GL_QUADS)
    for verts, norm in [
        # Frente  (+Z)
        ([(1.0,1.0,-0.5,-0.5, 0.5), (3.0,1.0, 0.5,-0.5, 0.5),
          (3.0,3.0, 0.5, 0.5, 0.5), (1.0,3.0,-0.5, 0.5, 0.5)], (0, 0, 1)),
        # Trás    (-Z)
        ([(3.0,1.0,-0.5,-0.5,-0.5), (3.0,3.0,-0.5, 0.5,-0.5),
          (1.0,3.0, 0.5, 0.5,-0.5), (1.0,1.0, 0.5,-0.5,-0.5)], (0, 0,-1)),
        # Cima    (+Y)
        ([(1.0,3.0,-0.5, 0.5,-0.5), (1.0,1.0,-0.5, 0.5, 0.5),
          (3.0,1.0, 0.5, 0.5, 0.5), (3.0,3.0, 0.5, 0.5,-0.5)], (0, 1, 0)),
        # Baixo   (-Y)
        ([(3.0,3.0,-0.5,-0.5,-0.5), (1.0,3.0, 0.5,-0.5,-0.5),
          (1.0,1.0, 0.5,-0.5, 0.5), (3.0,1.0,-0.5,-0.5, 0.5)], (0,-1, 0)),
        # Direita (+X)
        ([(1.0,1.0, 0.5,-0.5,-0.5), (1.0,3.0, 0.5, 0.5,-0.5),
          (3.0,3.0, 0.5, 0.5, 0.5), (3.0,1.0, 0.5,-0.5, 0.5)], (1, 0, 0)),
        # Esquerda(-X)  ← corrigida em relação à Atividade 1
        ([(1.0,1.0,-0.5,-0.5,-0.5), (3.0,1.0,-0.5,-0.5, 0.5),
          (3.0,3.0,-0.5, 0.5, 0.5), (1.0,3.0,-0.5, 0.5,-0.5)], (-1, 0, 0)),
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
        f"Atividade 2: Texture Wrapping  |  [1/{len(wrap_modes)}] {wrap_names[0]}",
        None, None
    )
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)
    glfw.set_key_callback(window, key_callback)   # ← novo callback de teclado

    init()
    texture_id = criar_textura_checkerboard()

    # Instrução no terminal
    print("=" * 55)
    print("  Atividade 2 – Texture Wrapping")
    print("=" * 55)
    print("  [ESPAÇO]  → alterna o modo de wrap")
    print("  [Mouse]   → arrasta para rotacionar o cubo")
    print("=" * 55)
    for i, (n, d) in enumerate(zip(wrap_names, wrap_desc)):
        print(f"  Modo {i+1}: {n}")
        print(f"          {d}")
    print("=" * 55)
    print(f"\n  Modo atual: {wrap_names[current_mode]}")

    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    main()