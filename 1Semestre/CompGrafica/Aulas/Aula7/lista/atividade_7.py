import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

# ------------------------------------------------------------------
# Estado da câmera
# ------------------------------------------------------------------
rx = ry = 0.0        # ângulos de rotação (Orbit — botão esquerdo)
pan_x = pan_y = 0.0  # deslocamento em X e Y (Pan — botão do meio)
cam_z = -5.0         # distância da câmera no eixo Z
#
# ATENÇÃO: a variável de câmera foi renomeada de 'z' para 'cam_z'.
# O nome 'z' era sobrescrito silenciosamente dentro do loop
# "for u, v, x, y, z in verts", corrompendo a posição da câmera
# a partir do segundo frame.
# ------------------------------------------------------------------

left_down   = False
middle_down = False
last_x = last_y = 0.0


def mouse_button(window, button, action, mods):
    global left_down, middle_down, last_x, last_y

    if button == glfw.MOUSE_BUTTON_LEFT:
        left_down = action == glfw.PRESS
    elif button == glfw.MOUSE_BUTTON_MIDDLE:
        middle_down = action == glfw.PRESS

    # Registra a posição do cursor sempre que qualquer botão é pressionado
    if action == glfw.PRESS:
        last_x, last_y = glfw.get_cursor_pos(window)


def cursor_pos(window, xpos, ypos):
    """
    Desacoplamento de Rotação e Translação (conceito do PDF):

    Botão ESQUERDO → Orbit (girar o cubo em torno do próprio centro)
    Botão do MEIO  → Pan   (deslizar a cena em X e Y)

    A ordem no render() garante o desacoplamento:
      1. glTranslatef(pan_x, pan_y, cam_z)  ← move o universo (Pan + Zoom)
      2. glRotatef(rx, ...)                  ← gira em torno do centro local
      3. glRotatef(ry, ...)
    Se a ordem fosse invertida, a rotação "arrastaria" o cubo para
    fora do centro e ele passaria a orbitar a origem do mundo.
    """
    global rx, ry, pan_x, pan_y, last_x, last_y

    dx = xpos - last_x
    dy = ypos - last_y

    if left_down:
        # Orbit: altera os ângulos de rotação
        ry += dx * 0.5
        rx += dy * 0.5

    elif middle_down:
        # Pan: desloca a cena nos eixos globais X e Y
        pan_x += dx * 0.01
        pan_y -= dy * 0.01   # Y invertido: tela cresce para baixo, 3D cresce para cima

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

    # ------------------------------------------------------------------
    # Ordem correta (lida de baixo para cima pela GPU):
    #   1º → Rotação  (gira o cubo em torno do seu centro)
    #   2º → Translação Pan + Zoom  (move no espaço global)
    # Escrevemos na ordem inversa porque OpenGL empilha as matrizes.
    # ------------------------------------------------------------------
    glTranslatef(pan_x, pan_y, cam_z)   # Pan (X, Y) + Zoom (Z)
    glRotatef(rx, 1, 0, 0)              # Orbit vertical
    glRotatef(ry, 0, 1, 0)              # Orbit horizontal

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
        # Esquerda(-X)  ← corrigida: sem UV duplicado, usando vx/vy/vz
        ([(0.0,0.0,-0.5,-0.5,-0.5), (1.0,0.0,-0.5,-0.5, 0.5),
          (1.0,1.0,-0.5, 0.5, 0.5), (0.0,1.0,-0.5, 0.5,-0.5)], (-1, 0, 0)),
    ]:
        glNormal3f(*norm)
        # Variáveis renomeadas para vx, vy, vz — evita conflito com cam_z global
        for u, v, vx, vy, vz in verts:
            glTexCoord2f(u, v)
            glVertex3f(vx, vy, vz)
    glEnd()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(
        800, 600,
        'Atividade 7: Câmera Pan  |  [Esq] Orbit  [Meio] Pan',
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
    # Explicação didática no terminal
    # ------------------------------------------------------------------
    print("=" * 62)
    print("  Atividade 7 – Câmera Pan (Arrastar a Tela)")
    print("=" * 62)
    print()
    print("  Conceito: Desacoplamento de Rotação e Translação")
    print()
    print("  O segredo está na ORDEM das transformações no render():")
    print()
    print("    glTranslatef(pan_x, pan_y, cam_z)  ← 1º: move o universo")
    print("    glRotatef(rx, 1, 0, 0)              ← 2º: gira em X")
    print("    glRotatef(ry, 0, 1, 0)              ← 3º: gira em Y")
    print()
    print("  Ordem CORRETA (desacoplada):")
    print("    O cubo gira sempre em torno do seu próprio centro,")
    print("    independentemente de onde ele está na tela.")
    print()
    print("  Ordem ERRADA (acoplada):")
    print("    Rotação antes da translação faria o cubo 'orbitar'")
    print("    a origem do mundo como um planeta amarrado a um barbante.")
    print()
    print("  CORREÇÃO CRÍTICA aplicada neste código:")
    print("    A variável global 'z' foi renomeada para 'cam_z'.")
    print("    O loop 'for u, v, x, y, z in verts' sobrescrevia")
    print("    o 'z' global a cada iteração, corrompendo a câmera.")
    print("    Agora o loop usa 'vx, vy, vz' para os vértices.")
    print()
    print("  [Mouse Esq]  Arrasta → Orbit (girar o cubo)")
    print("  [Mouse Meio] Arrasta → Pan   (deslizar a cena)")
    print("=" * 62)

    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    main()