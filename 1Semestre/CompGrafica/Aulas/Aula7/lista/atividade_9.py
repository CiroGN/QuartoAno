import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

# ------------------------------------------------------------------
# Estado de rotação (Orbit — botão esquerdo + arrastar)
# ------------------------------------------------------------------
rx = ry = 0.0
mouse_down  = False
last_x = last_y = 0.0

# ------------------------------------------------------------------
# Estado da câmera (Zoom animado via LERP — duplo clique)
#
# camera_z → onde a câmera ESTÁ agora (atualizado a cada frame)
# target_z → onde a câmera QUER chegar (muda no duplo clique)
#
# O evento do mouse não move a câmera diretamente; ele apenas
# muda a "intenção" (target_z). Quem faz o deslizamento suave é
# a fórmula LERP no loop principal — conceito de Programação
# Reativa a Estados (base do iOS, Android e Unreal Engine).
# ------------------------------------------------------------------
camera_z  = -5.0
target_z  = -5.0
ZOOM_FAR  = -5.0   # posição "visão geral"
ZOOM_NEAR = -2.0   # posição "inspeção detalhada"

# Cronômetro para detecção de duplo clique
last_click = 0.0
DOUBLE_CLICK_MS = 0.3   # janela de tempo em segundos


def mouse_button(window, button, action, mods):
    global mouse_down, last_x, last_y, last_click, target_z

    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            current = glfw.get_time()

            # ----------------------------------------------------------
            # Detecção de duplo clique:
            # 1. Guarda o tempo do 1º clique em last_click.
            # 2. No 2º clique, calcula a diferença.
            # 3. Se < 0.3s → duplo clique detectado.
            # ----------------------------------------------------------
            if current - last_click < DOUBLE_CLICK_MS:
                # Alterna o ALVO (não a posição imediata da câmera!)
                if target_z == ZOOM_FAR:
                    target_z = ZOOM_NEAR
                    print("[DUPLO CLIQUE] Focando no bloco  → target_z =", ZOOM_NEAR)
                else:
                    target_z = ZOOM_FAR
                    print("[DUPLO CLIQUE] Visão geral       → target_z =", ZOOM_FAR)

            last_click  = current
            mouse_down  = True
            last_x, last_y = glfw.get_cursor_pos(window)

        else:   # RELEASE
            mouse_down = False


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


def update():
    """
    Atualiza o estado da câmera a cada frame (separado do render).

    LERP Assintótico (Suavização Exponencial):
      camera_z += (target_z - camera_z) * velocidade

    A câmera percorre uma PORCENTAGEM da distância restante a cada
    frame — começa rápida e vai freando ao se aproximar do alvo.
    Não precisa de cronômetro de animação; converge naturalmente.

    Fórmula geral:  Atual = Atual + (Alvo - Atual) * t
    Onde t (velocidade) vai de 0.0 (parado) a 1.0 (instantâneo).
    """
    global camera_z
    velocidade = 0.05
    camera_z += (target_z - camera_z) * velocidade


def render(texture_id):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, camera_z)
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
        # Esquerda(-X)  ← corrigida: sem UV duplicado; loop usa vx,vy,vz
        ([(0.0,0.0,-0.5,-0.5,-0.5), (1.0,0.0,-0.5,-0.5, 0.5),
          (1.0,1.0,-0.5, 0.5, 0.5), (0.0,1.0,-0.5, 0.5,-0.5)], (-1, 0, 0)),
    ]:
        glNormal3f(*norm)
        # Variáveis de vértice nomeadas vx,vy,vz para não conflitar
        # com nenhuma variável de câmera ou escopo externo
        for u, v, vx, vy, vz in verts:
            glTexCoord2f(u, v)
            glVertex3f(vx, vy, vz)
    glEnd()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(
        800, 600,
        'Atividade 9: Double Click Zoom  |  [Duplo Clique] Aproxima/Afasta',
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
    print("  Atividade 9 – Inspeção Detalhada (Double Click Zoom)")
    print("=" * 62)
    print()
    print("  Três conceitos conectados:")
    print()
    print("  1. CRONÔMETRO (Detecção de Duplo Clique)")
    print("     glfw.get_time() retorna segundos desde o início.")
    print("     Se o intervalo entre dois cliques < 0.3s → duplo clique.")
    print()
    print("  2. MUDANÇA DE ESTADO (Reatividade)")
    print("     O clique não move a câmera — muda apenas o ALVO.")
    print(f"     target_z alterna entre {ZOOM_FAR} (longe) e {ZOOM_NEAR} (perto).")
    print("     Quem move a câmera é a fórmula LERP no loop principal.")
    print()
    print("  3. LERP ASSINTÓTICO (Suavização Exponencial)")
    print("     camera_z += (target_z - camera_z) * 0.05")
    print("     A câmera percorre 5% da distância restante a cada frame.")
    print("     Efeito: começa rápida, freia suavemente ao chegar no alvo.")
    print("     Sem cronômetro de animação — converge naturalmente.")
    print()
    print("  SEPARAÇÃO DE RESPONSABILIDADES:")
    print("     update() → atualiza o estado (LERP)")
    print("     render() → desenha a cena (sem modificar estado)")
    print()
    print("  [Duplo Clique] Alterna zoom perto/longe")
    print("  [Mouse Esq]    Arrasta para rotacionar o cubo")
    print("=" * 62)
    print(f"\n  Estado inicial: camera_z={camera_z}  target_z={target_z}")

    while not glfw.window_should_close(window):
        update()           # 1. atualiza estado (LERP da câmera)
        render(texture_id) # 2. desenha com o estado atualizado
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    main()