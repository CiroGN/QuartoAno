import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

rx     = ry    = 0.0
zoom_z = -5.0          # posição Z inicial (câmera afastada)
ZOOM_MIN = -15.0       # limite máximo de afastamento
ZOOM_MAX =  -2.0       # limite mínimo (evita atravessar o cubo)

mouse_down      = False
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


def scroll(window, xoffset, yoffset):
    """
    Callback do scroll (rodinha do mouse).

    yoffset:  +1 → scroll para frente (aproxima)
              -1 → scroll para trás  (afasta)

    Lógica de zoom (ilusão de câmera):
      A câmera fica parada na origem. O que movemos é o universo
      inteiro no eixo Z via glTranslatef. Aumentar zoom_z em direção
      a zero aproxima o cubo; diminuir afasta.

    Limites lógicos (Clamp):
      ZOOM_MAX = -2.0  → não atravessa o cubo (Near Clipping)
      ZOOM_MIN = -15.0 → não some no horizonte
    """
    global zoom_z
    velocidade = 0.5
    zoom_z += yoffset * velocidade

    # Clamp: garante que zoom_z fique entre ZOOM_MIN e ZOOM_MAX
    if zoom_z > ZOOM_MAX:
        zoom_z = ZOOM_MAX
        print("[ZOOM] Limite proximo atingido! (Near Clipping evitado)")
    elif zoom_z < ZOOM_MIN:
        zoom_z = ZOOM_MIN
        print("[ZOOM] Limite distante atingido!")
    else:
        print(f"[ZOOM] zoom_z = {zoom_z:.2f}  "
              f"(min={ZOOM_MIN}, max={ZOOM_MAX})")


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

    # zoom_z controla a "ilusão de câmera" — empurra o universo no eixo Z
    glTranslatef(0.0, 0.0, zoom_z)

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
    if not glfw.init():
        return

    window = glfw.create_window(
        800, 600,
        'Atividade 6: Zoom com Scroll  |  [Scroll] Aproxima/Afasta',
        None, None
    )
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)
    glfw.set_scroll_callback(window, scroll)      # ← callback do scroll

    init()
    texture_id = criar_textura_checkerboard()

    # ------------------------------------------------------------------
    # Explicação didática no terminal
    # ------------------------------------------------------------------
    print("=" * 60)
    print("  Atividade 6 – Zoom Interativo com Scroll")
    print("=" * 60)
    print()
    print("  A ilusao do Zoom no OpenGL classico:")
    print("    A camara esta SEMPRE na origem (0, 0, 0).")
    print("    Para 'aproximar', empurramos o universo inteiro")
    print("    no eixo Z usando glTranslatef(0, 0, zoom_z).")
    print()
    print("  Scroll para frente → zoom_z sobe em direcao a 0")
    print("    Ex: -5.0 → -4.5 → -4.0  (cubo se aproxima)")
    print()
    print("  Scroll para tras  → zoom_z desce para negativo")
    print("    Ex: -5.0 → -5.5 → -6.0  (cubo se afasta)")
    print()
    print("  Limites logicos (Clamp):")
    print(f"    ZOOM_MAX = {ZOOM_MAX}  → evita Near Clipping")
    print(f"      (se Z > {ZOOM_MAX}, o OpenGL corta a face frontal do cubo)")
    print(f"    ZOOM_MIN = {ZOOM_MIN} → evita sumir no horizonte")
    print()
    print("  [Scroll]    Aproxima / Afasta")
    print("  [Mouse Esq] Arrasta para rotacionar o cubo")
    print("=" * 60)
    print(f"\n  Zoom inicial: zoom_z = {zoom_z}")

    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    main()