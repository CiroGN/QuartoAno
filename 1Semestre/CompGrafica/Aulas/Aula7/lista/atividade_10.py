import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_agua


def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.1, 0.15, 0.25, 1.0)    # azul-escuro (fundo aquático)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)


def render(texture_id):
    # ------------------------------------------------------------------
    # UV Scrolling — o "truque" dos jogos clássicos
    #
    # glfw.get_time() cresce infinitamente (0.0, 0.1, 0.2 ...).
    # Somamos esse valor ao eixo U (horizontal) a cada frame.
    # Como GL_REPEAT está ativo, quando U passa de 1.0 o OpenGL
    # recomeça a textura do zero — criando um loop visual infinito.
    #
    # * 0.5 = velocidade; aumente para água mais rápida.
    # ------------------------------------------------------------------
    deslocamento_u = glfw.get_time() * 0.5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Posiciona a câmera: desce 1 unidade, afasta 8, inclina 45° para ver o chão
    glTranslatef(0.0, -1.0, -8.0)
    glRotatef(45.0, 1.0, 0.0, 0.0)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    # ------------------------------------------------------------------
    # GL_REPEAT é OBRIGATÓRIO para o UV Scrolling funcionar.
    #
    # Sem ele (ex: GL_CLAMP_TO_EDGE), quando U ultrapassa 1.0 o OpenGL
    # estica a borda em vez de repetir — a água "congela" nas bordas
    # em vez de fluir continuamente.
    #
    # Configuramos aqui (e não só no carregamento) para garantir que
    # nenhum outro código sobrescreva o parâmetro desta textura.
    # ------------------------------------------------------------------
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # eixo U → flui
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # eixo V → repetido

    # Filtro bilinear: suaviza a textura ao ser ampliada/reduzida
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # ------------------------------------------------------------------
    # Plano da água (chão horizontal)
    #
    # UVs vão de 0.0 a 3.0 → a textura repete 3x em ambos os eixos.
    # O deslocamento_u é somado APENAS ao eixo U (horizontal),
    # fazendo a água fluir para a direita.
    # Para fluir para a frente/trás, some ao V em vez do U.
    # ------------------------------------------------------------------
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)   # normal apontando para cima (face superior)

    # Canto traseiro-esquerdo
    glTexCoord2f(0.0 + deslocamento_u, 0.0)
    glVertex3f(-3.0, 0.0,  3.0)

    # Canto traseiro-direito
    glTexCoord2f(3.0 + deslocamento_u, 0.0)
    glVertex3f( 3.0, 0.0,  3.0)

    # Canto frontal-direito
    glTexCoord2f(3.0 + deslocamento_u, 3.0)
    glVertex3f( 3.0, 0.0, -3.0)

    # Canto frontal-esquerdo
    glTexCoord2f(0.0 + deslocamento_u, 3.0)
    glVertex3f(-3.0, 0.0, -3.0)

    glEnd()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(
        800, 600,
        'Atividade 10: Água Deslizante (UV Scrolling)',
        None, None
    )
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    init()
    texture_id = criar_textura_agua()

    # ------------------------------------------------------------------
    # Explicação didática no terminal
    # ------------------------------------------------------------------
    print("=" * 62)
    print("  Atividade 10 – Água Deslizante (Animação UV / UV Scrolling)")
    print("=" * 62)
    print()
    print("  Técnica usada em: Super Mario 64 (Lethal Lava Land),")
    print("  Zelda: Ocarina of Time, Minecraft, e jogos modernos.")
    print()
    print("  O TRUQUE:")
    print("    A geometria (o plano 3D) fica TOTALMENTE PARADA.")
    print("    O que se move é a leitura da textura — as UVs.")
    print("    A cada frame somamos glfw.get_time() * 0.5 ao eixo U.")
    print()
    print("  Por que funciona sem travar?")
    print("    GL_REPEAT: quando U passa de 1.0, o OpenGL recomeça")
    print("    a imagem do zero — loop visual infinito e perfeito.")
    print("    Sem GL_REPEAT, a água 'congela' nas bordas (CLAMP).")
    print()
    print("  Custo computacional: ZERO vértices alterados.")
    print("    A matemática ocorre inteiramente na GPU durante o")
    print("    mapeamento de textura — não sobrecarrega a CPU.")
    print()
    print("  Variações possíveis:")
    print("    → Some ao V para fluir para frente/trás")
    print("    → Some a ambos U e V para movimento diagonal")
    print("    → Use velocidades diferentes em U e V para turbulência")
    print()
    print("  [Janela] Observe a água fluindo para a direita.")
    print("=" * 62)

    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    main()