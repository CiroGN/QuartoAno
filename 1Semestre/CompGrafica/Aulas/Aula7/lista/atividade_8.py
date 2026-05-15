import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_terra

# ------------------------------------------------------------------
# Posição da luz — atualizada pelo movimento do mouse
# ------------------------------------------------------------------
light_x = 0.0
light_y = 0.0


def cursor_pos(window, xpos, ypos):
    """
    Converte coordenadas de tela (pixels) para coordenadas do mundo 3D.

    Fórmula do PDF:
      X_norm = (X_mouse / Largura)  * 2 - 1   →  escala para [-1, +1]
      Y_norm = -((Y_mouse / Altura) * 2 - 1)  →  inverte Y (tela desce, 3D sobe)

    Em seguida multiplicamos pelo alcance da câmera (4 unidades em X, 3 em Y)
    para que a luz cubra toda a área visível da esfera.
    """
    global light_x, light_y
    light_x =  (xpos / 800.0) * 2.0 - 1.0
    light_x *= 4.0                              # escala: câmera vê de -4 a +4 em X
    light_y = -((ypos / 600.0) * 2.0 - 1.0)
    light_y *= 3.0                              # escala: câmera vê de -3 a +3 em Y


def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)                  # liga o motor de iluminação
    glEnable(GL_LIGHT0)                    # ativa a lâmpada 0
    glEnable(GL_COLOR_MATERIAL)            # textura interage com a iluminação

    # GL_COLOR_MATERIAL: o OpenGL usa a cor da textura como cor difusa do material
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glClearColor(0.02, 0.02, 0.08, 1.0)   # fundo azul-escuro (espaço)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

    # ------------------------------------------------------------------
    # Configuração da GL_LIGHT0
    # glLightfv é a forma correta de passar vetores float para o OpenGL.
    # glLight (sem o 'fv') é um alias Python que pode falhar em conversão.
    # ------------------------------------------------------------------
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.05, 0.05, 0.10, 1.0))  # ambiente mínimo
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.00, 1.00, 0.95, 1.0))  # luz branca-quente
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.80, 0.80, 0.80, 1.0))  # brilho especular

    # Material da esfera: define como ela reflete a luz
    glMaterialfv(GL_FRONT, GL_SPECULAR,  (0.3, 0.3, 0.3, 1.0))
    glMaterialf (GL_FRONT, GL_SHININESS, 40.0)


def render(texture_id, quad):
    """
    quad é criado UMA VEZ em main() e reutilizado a cada frame.
    Criar gluNewQuadric() dentro do render() vazaria memória na GPU
    (60+ objetos não destruídos por segundo).
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)

    # ------------------------------------------------------------------
    # Posiciona a luz APÓS o glLoadIdentity / glTranslatef.
    # W = 1.0 → luz POSICIONAL (lanterna com posição física na cena).
    # W = 0.0 → luz direcional (sol, sem posição, só direção).
    # Z = 3.0 → a luz fica à frente da esfera (entre câmera e Terra).
    # ------------------------------------------------------------------
    glLightfv(GL_LIGHT0, GL_POSITION, (light_x, light_y, 3.0, 1.0))

    glBindTexture(GL_TEXTURE_2D, texture_id)
    gluSphere(quad, 1.0, 64, 64)   # raio=1, 64 fatias de resolução


def main():
    if not glfw.init():
        return

    window = glfw.create_window(
        800, 600,
        'Atividade 8: Lanterna do Mouse (Spotlight Móvel)',
        None, None
    )
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, cursor_pos)

    init()
    texture_id = criar_textura_terra()

    # ------------------------------------------------------------------
    # Quadric criado UMA VEZ e destruído ao final — sem memory leak
    # gluQuadricNormals(GLU_SMOOTH): gera normais suaves para que o
    # OpenGL calcule o gradiente de luz corretamente na curvatura da esfera.
    # gluQuadricTexture(GL_TRUE): mapeia as coordenadas UV automaticamente.
    # ------------------------------------------------------------------
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)

    # ------------------------------------------------------------------
    # Explicação didática no terminal
    # ------------------------------------------------------------------
    print("=" * 62)
    print("  Atividade 8 – A Lanterna do Mouse (Spotlight Móvel)")
    print("=" * 62)
    print()
    print("  Conceito: Screen-to-World Space (Tela → Mundo 3D)")
    print()
    print("  Fórmula de conversão:")
    print("    X_norm = (X_mouse / 800) * 2 - 1  →  [-1, +1]")
    print("    Y_norm = -((Y_mouse / 600) * 2 - 1)  (Y invertido)")
    print("    luz_x  = X_norm * 4.0  (escala para o mundo)")
    print("    luz_y  = Y_norm * 3.0")
    print()
    print("  A lâmpada GL_LIGHT0 com W=1.0 é POSICIONAL:")
    print("    Tem posição física (X, Y, Z) dentro da cena.")
    print("    Irradia luz em todas as direções a partir desse ponto.")
    print("    (W=0.0 seria direcional, como o Sol — sem posição)")
    print()
    print("  gluQuadricNormals(GLU_SMOOTH):")
    print("    Gera normais suaves na esfera para que o OpenGL")
    print("    calcule o gradiente de luz na curvatura — base dos")
    print("    Normal Maps em motores modernos.")
    print()
    print("  [Mouse] Move a luz sobre a superfície da Terra.")
    print("=" * 62)

    while not glfw.window_should_close(window):
        render(texture_id, quad)
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Libera o objeto quadric da memória
    gluDeleteQuadric(quad)
    glfw.terminate()


if __name__ == '__main__':
    main()