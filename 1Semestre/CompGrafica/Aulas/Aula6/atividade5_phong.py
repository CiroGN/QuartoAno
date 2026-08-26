import glfw
from OpenGL.GL import *
import math

# ── Geometria ─────────────────────────────────────────────────────────────────

def gerar_esfera(raio, subdivisoes_h, subdivisoes_v):
    vertices = []
    for v in range(subdivisoes_v + 1):
        theta = v * math.pi / subdivisoes_v
        for h in range(subdivisoes_h + 1):
            phi = h * 2 * math.pi / subdivisoes_h
            x = raio * math.sin(theta) * math.cos(phi)
            y = raio * math.cos(theta)
            z = raio * math.sin(theta) * math.sin(phi)
            vertices.append((x, y, z))
    triangulos = []
    for v in range(subdivisoes_v):
        for h in range(subdivisoes_h):
            p1 = v * (subdivisoes_h + 1) + h
            p2 = p1 + subdivisoes_h + 1
            triangulos.append((p1, p2, p1 + 1))
            triangulos.append((p2, p2 + 1, p1 + 1))
    return vertices, triangulos


def calcula_normal(a, b, c):
    A = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
    B = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
    nx = A[1]*B[2] - A[2]*B[1]
    ny = A[2]*B[0] - A[0]*B[2]
    nz = A[0]*B[1] - A[1]*B[0]
    cx, cy, cz = (a[0]+b[0]+c[0])/3, (a[1]+b[1]+c[1])/3, (a[2]+b[2]+c[2])/3
    if nx*cx + ny*cy + nz*cz < 0:
        nx, ny, nz = -nx, -ny, -nz
    comp = math.sqrt(nx**2 + ny**2 + nz**2)
    if comp == 0:
        return (0, 0, 1)
    return (nx/comp, ny/comp, nz/comp)


# ── Iluminação de Phong com cor difusa e especular separadas ──────────────────
#
#  NOVIDADE DA ATIVIDADE 5:
#  A função agora recebe duas cores:
#    cor_difusa   → cor "base" do material (ambiente + difusa)
#    cor_especular → cor do reflexo (brilho especular)
#
#  Isso permite criar materiais onde o brilho tem cor completamente diferente
#  do objeto — efeito "alienígena" ou "holográfico".

def aplicar_phong(normal, vertice, pos_luz, pos_camera,
                  cor_difusa, cor_especular, brilho):

    nx, ny, nz = normal

    # Vetor L (superfície → luz), normalizado
    lx = pos_luz[0] - vertice[0]
    ly = pos_luz[1] - vertice[1]
    lz = pos_luz[2] - vertice[2]
    comp_l = math.sqrt(lx**2 + ly**2 + lz**2)
    lx, ly, lz = lx/comp_l, ly/comp_l, lz/comp_l

    # Vetor V (superfície → câmera), normalizado
    vx = pos_camera[0] - vertice[0]
    vy = pos_camera[1] - vertice[1]
    vz = pos_camera[2] - vertice[2]
    comp_v = math.sqrt(vx**2 + vy**2 + vz**2)
    vx, vy, vz = vx/comp_v, vy/comp_v, vz/comp_v

    # Componentes escalares
    ambiente = 0.1
    dot_nl   = max(0.0, nx*lx + ny*ly + nz*lz)
    difusa   = 0.6 * dot_nl

    # Vetor R de reflexão
    rx = 2*dot_nl*nx - lx
    ry = 2*dot_nl*ny - ly
    rz = 2*dot_nl*nz - lz
    dot_rv   = max(0.0, rx*vx + ry*vy + rz*vz)
    especular = 0.8 * (dot_rv ** brilho) if dot_nl > 0 else 0.0

    # Cor final:
    #   parte difusa  → modulada pela cor base do objeto
    #   parte especular → modulada pela cor do reflexo (pode ser diferente!)
    fator_diff = ambiente + difusa
    return (
        min(1.0, cor_difusa[0] * fator_diff + cor_especular[0] * especular),
        min(1.0, cor_difusa[1] * fator_diff + cor_especular[1] * especular),
        min(1.0, cor_difusa[2] * fator_diff + cor_especular[2] * especular),
    )


# ── Materiais disponíveis (teclas 1-4) ───────────────────────────────────────
#
#   Cada material tem: nome, cor_difusa, cor_especular, brilho

MATERIAIS = [
    {
        "nome":          "Alienígena (corpo roxo / brilho verde néon)",
        "cor_difusa":    (0.45, 0.05, 0.80),   # roxo escuro
        "cor_especular": (0.10, 1.00, 0.30),   # verde néon
        "brilho":        64,
    },
    {
        "nome":          "Holográfico (azul / brilho dourado)",
        "cor_difusa":    (0.05, 0.30, 0.80),   # azul
        "cor_especular": (1.00, 0.85, 0.10),   # dourado
        "brilho":        128,
    },
    {
        "nome":          "Plasma (laranja / brilho ciano)",
        "cor_difusa":    (0.90, 0.35, 0.05),   # laranja
        "cor_especular": (0.00, 0.95, 0.95),   # ciano elétrico
        "brilho":        32,
    },
    {
        "nome":          "Clássico Phong (vermelho / brilho branco)",
        "cor_difusa":    (0.80, 0.10, 0.10),   # vermelho
        "cor_especular": (1.00, 1.00, 1.00),   # branco (comportamento padrão)
        "brilho":        32,
    },
]

material_atual = 0   # índice do material selecionado


# ── Callback de teclado ───────────────────────────────────────────────────────

def key_callback(window, key, scancode, action, mods):
    global material_atual
    if action == glfw.PRESS:
        if key == glfw.KEY_1: material_atual = 0
        if key == glfw.KEY_2: material_atual = 1
        if key == glfw.KEY_3: material_atual = 2
        if key == glfw.KEY_4: material_atual = 3
        m = MATERIAIS[material_atual]
        print(f"  [{material_atual+1}] {m['nome']}")
        print(f"      Difusa   = {m['cor_difusa']}")
        print(f"      Especular= {m['cor_especular']}  |  α = {m['brilho']}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Phong – Materiais alienígenas | teclas 1-4", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.5, 1.5, -1.5, 1.5, -5.0, 5.0)
    glMatrixMode(GL_MODELVIEW)

    vertices, triangulos = gerar_esfera(0.8, 40, 40)

    pos_luz    = (2.0, 2.0, 2.0)
    pos_camera = (0.0, 0.0, 5.0)

    angulo = 0
    glClearColor(0.05, 0.05, 0.08, 1.0)

    print("=" * 55)
    print("  Atividade 5 – Cor difusa ≠ cor especular")
    print("  Tecla 1 → Alienígena  (roxo + verde néon)")
    print("  Tecla 2 → Holográfico (azul  + dourado)")
    print("  Tecla 3 → Plasma      (laranja + ciano)")
    print("  Tecla 4 → Clássico    (vermelho + branco)")
    print("=" * 55)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotatef(20, 1, 0, 0)
        glRotatef(angulo, 0, 1, 0)
        angulo += 0.5

        m = MATERIAIS[material_atual]
        glfw.set_window_title(
            window,
            f"Atividade 5  |  [{material_atual+1}] {m['nome']}  |  teclas 1-4"
        )

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_TRIANGLES)
        for tri in triangulos:
            v1, v2, v3 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]
            normal = calcula_normal(v1, v2, v3)
            cor = aplicar_phong(
                normal, v1, pos_luz, pos_camera,
                m["cor_difusa"], m["cor_especular"], m["brilho"]
            )
            glColor3f(*cor)
            glVertex3f(*v1)
            glVertex3f(*v2)
            glVertex3f(*v3)
        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
