import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_terra, criar_textura_nuvens


def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)            # textura interage com a iluminação

    # GL_COLOR_MATERIAL: usa a cor da textura como cor difusa do material
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glClearColor(0.0, 0.0, 0.05, 1.0)     # preto-azulado (espaço)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

    # ------------------------------------------------------------------
    # glLightfv é a forma correta para passar vetores float ao OpenGL.
    # glLight (sem 'fv') é um alias Python que pode falhar na conversão.
    #
    # A POSIÇÃO da luz NÃO é configurada aqui — deve ficar no render()
    # após glLoadIdentity(), para ser interpretada no espaço correto.
    # ------------------------------------------------------------------
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.10, 0.10, 0.15, 1.0))  # ambiente mínimo
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.00, 0.98, 0.90, 1.0))  # luz solar branca-quente
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.50, 0.50, 0.50, 1.0))

    # Material das esferas
    glMaterialfv(GL_FRONT, GL_SPECULAR,  (0.2, 0.2, 0.2, 1.0))
    glMaterialf (GL_FRONT, GL_SHININESS, 30.0)


def render(texture_terra, texture_nuvens, quad_terra, quad_nuvens):
    """
    quad_terra e quad_nuvens são criados UMA VEZ em main() e
    reutilizados a cada frame — sem memory leak.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)

    # ------------------------------------------------------------------
    # Luz posicionada AQUI, após glLoadIdentity, no espaço da câmera.
    # W = 0.0 → luz DIRECIONAL (como o Sol — vem do infinito).
    # Posicionada antes do PushMatrix para ficar no espaço global.
    # ------------------------------------------------------------------
    glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 5.0, 5.0, 0.0))

    tempo      = glfw.get_time()
    rot_terra  = tempo * 20.0   # Terra gira mais rápido
    rot_nuvens = tempo *  5.0   # Nuvens giram mais devagar

    # ------------------------------------------------------------------
    # 1. ESFERA DA TERRA (sólida)
    # glPushMatrix → aplica rotação exclusiva → desenha → glPopMatrix
    # O Pop descarta a rotação da Terra antes de desenhar as nuvens.
    # ------------------------------------------------------------------
    glBindTexture(GL_TEXTURE_2D, texture_terra)
    glPushMatrix()
    glRotatef(rot_terra, 0.0, 1.0, 0.0)
    gluSphere(quad_terra, 1.0, 64, 64)     # raio 1.0, alta resolução
    glPopMatrix()

    # ------------------------------------------------------------------
    # 2. ESFERA DAS NUVENS (transparente — 1% maior que a Terra)
    #
    # Por que 1.01 e não 1.0?
    # Se as duas esferas tiverem o mesmo raio, o Z-Buffer não consegue
    # decidir qual está na frente, causando Z-Fighting (flickering).
    # 1.01 garante que as nuvens formem uma "casca" sobre a Terra.
    #
    # GL_BLEND com GL_SRC_ALPHA / GL_ONE_MINUS_SRC_ALPHA:
    # "Cor final = cor_nuvem * alpha_nuvem + cor_terra * (1 - alpha_nuvem)"
    # Pixels transparentes do PNG deixam a Terra aparecer por baixo.
    # ------------------------------------------------------------------
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindTexture(GL_TEXTURE_2D, texture_nuvens)
    glPushMatrix()
    glRotatef(rot_nuvens, 0.0, 1.0, 0.0)
    gluSphere(quad_nuvens, 1.01, 64, 64)   # raio 1.01 → casca externa
    glPopMatrix()

    glDisable(GL_BLEND)    # desliga para não afetar outros objetos futuros


def main():
    if not glfw.init():
        return

    window = glfw.create_window(
        800, 600,
        'Atividade 11: Terra e Nuvens (Multi-texturing Analógico)',
        None, None
    )
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    init()

    texture_terra  = criar_textura_terra()
    texture_nuvens = criar_textura_nuvens()

    # ------------------------------------------------------------------
    # Quadrics criados UMA VEZ e destruídos ao final.
    # Criar gluNewQuadric() dentro do render() = 120+ objetos por segundo
    # não destruídos → memory leak progressivo na GPU.
    # ------------------------------------------------------------------
    quad_terra = gluNewQuadric()
    gluQuadricNormals(quad_terra, GLU_SMOOTH)   # normais suaves para iluminação
    gluQuadricTexture(quad_terra, GL_TRUE)       # mapeamento UV automático

    quad_nuvens = gluNewQuadric()
    gluQuadricNormals(quad_nuvens, GLU_SMOOTH)
    gluQuadricTexture(quad_nuvens, GL_TRUE)

    # ------------------------------------------------------------------
    # Explicação didática no terminal
    # ------------------------------------------------------------------
    print("=" * 62)
    print("  Atividade 11 – Terra e Nuvens (Multi-texturing Analógico)")
    print("=" * 62)
    print()
    print("  Técnica: duas esferas sobrepostas com texturas diferentes.")
    print()
    print("  1. ESFERA DA TERRA (raio 1.0)")
    print("     Textura sólida do mapa-múndi.")
    print("     Gira a 20°/s.")
    print()
    print("  2. ESFERA DAS NUVENS (raio 1.01 — 1% maior)")
    print("     Textura PNG com canal Alpha (transparência).")
    print("     Gira a 5°/s — mais devagar que a Terra.")
    print()
    print("  Por que 1.01 e não 1.0?")
    print("    Mesmo raio → Z-Fighting: a GPU não decide qual esfera")
    print("    está na frente → tela pisca loucamente (flickering).")
    print("    0.01 de diferença garante a 'casca' de nuvens.")
    print()
    print("  GL_BLEND + GL_SRC_ALPHA / GL_ONE_MINUS_SRC_ALPHA:")
    print("    Fórmula de transparência padrão (Porter-Duff 'over').")
    print("    Pixels transparentes do PNG revelam a Terra por baixo.")
    print()
    print("  glPushMatrix / glPopMatrix:")
    print("    Isola a rotação de cada esfera.")
    print("    Sem o Pop, a rotação da Terra somaria com a das nuvens.")
    print()
    print("  [Janela] Terra gira mais rápido; nuvens deslizam devagar.")
    print("=" * 62)

    while not glfw.window_should_close(window):
        render(texture_terra, texture_nuvens, quad_terra, quad_nuvens)
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Libera os quadrics da memória da GPU
    gluDeleteQuadric(quad_terra)
    gluDeleteQuadric(quad_nuvens)
    glfw.terminate()


if __name__ == '__main__':
    main()