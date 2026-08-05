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


def normalizar(v):
    comp = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if comp == 0:
        return (0, 0, 1)
    return (v[0]/comp, v[1]/comp, v[2]/comp)


# ── Iluminação de Phong — suporta Point Light e Directional Light ─────────────
#
#  PONTO-CHAVE DA ATIVIDADE 7:
#
#  Point Light (luz pontual):
#    L é calculado por vértice: L = normalize(pos_luz - vertice)
#    → cada vértice recebe um L diferente, apontando para a mesma fonte.
#    → o brilho especular muda de posição conforme a esfera gira.
#
#  Directional Light (luz direcional / Sol):
#    L é um vetor CONSTANTE, igual para todos os vértices.
#    → simula uma fonte infinitamente distante (raios paralelos).
#    → o brilho especular fica "preso" na mesma região da esfera,
#      independente da posição dos vértices — como a luz do sol.

def aplicar_phong(normal, vertice, pos_camera, cor_base, brilho,
                  modo_direcional, direcao_luz, pos_luz):

    nx, ny, nz = normal

    # ── Vetor L ───────────────────────────────────────────────────────────────
    if modo_direcional:
        # Directional Light: vetor constante (direção oposta à direção da luz)
        lx, ly, lz = direcao_luz
    else:
        # Point Light: calculado por vértice
        dx = pos_luz[0] - vertice[0]
        dy = pos_luz[1] - vertice[1]
        dz = pos_luz[2] - vertice[2]
        lx, ly, lz = normalizar((dx, dy, dz))

    # Vetor V (superfície → câmera)
    vx = pos_camera[0] - vertice[0]
    vy = pos_camera[1] - vertice[1]
    vz = pos_camera[2] - vertice[2]
    vx, vy, vz = normalizar((vx, vy, vz))

    # Componentes escalares
    ambiente  = 0.1
    dot_nl    = max(0.0, nx*lx + ny*ly + nz*lz)
    difusa    = 0.6 * dot_nl

    rx = 2*dot_nl*nx - lx
    ry = 2*dot_nl*ny - ly
    rz = 2*dot_nl*nz - lz
    dot_rv    = max(0.0, rx*vx + ry*vy + rz*vz)
    especular = 0.5 * (dot_rv ** brilho) if dot_nl > 0 else 0.0

    fator = ambiente + difusa + especular
    return (
        min(1.0, cor_base[0] * fator),
        min(1.0, cor_base[1] * fator),
        min(1.0, cor_base[2] * fator),
    )


# ── Estado global ─────────────────────────────────────────────────────────────

modo_direcional = False   # alterna com tecla SPACE

# Point Light: posição fixa
pos_luz = (2.0, 2.0, 2.0)

# Directional Light: direção da luz vindo de (-1,-1,-1), normalizada
# L aponta DA superfície PARA a luz → invertemos a direção
_dir = normalizar((1.0, 1.0, 1.0))   # direção oposta ao vetor (-1,-1,-1)
direcao_luz = _dir


# ── Callback de teclado ───────────────────────────────────────────────────────

def key_callback(window, key, scancode, action, mods):
    global modo_direcional
    if action == glfw.PRESS and key == glfw.KEY_SPACE:
        modo_direcional = not modo_direcional
        modo = "DIRECIONAL (Sol)" if modo_direcional else "PONTUAL (Point Light)"
        print(f"  Modo: {modo}")
        if modo_direcional:
            print(f"  Direção L constante = {tuple(round(v,3) for v in direcao_luz)}")
        else:
            print(f"  Posição da luz = {pos_luz}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Phong | SPACE alterna Point / Directional Light", None, None)
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

    pos_camera = (0.0, 0.0, 5.0)
    cor_esfera = (0.2, 0.6, 1.0)
    brilho     = 64

    angulo = 0
    glClearColor(0.05, 0.05, 0.08, 1.0)

    print("=" * 58)
    print("  Atividade 7 – Point Light vs Directional Light")
    print("  SPACE → alterna entre os dois modos")
    print()
    print("  Point Light:       L calculado por vértice (fonte pontual)")
    print("  Directional Light: L constante = (1,1,1) normalizado (Sol)")
    print()
    print("  Observe como o brilho especular se comporta nos dois modos")
    print("  enquanto a esfera gira.")
    print("=" * 58)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotatef(20, 1, 0, 0)
        glRotatef(angulo, 0, 1, 0)
        angulo += 0.5

        modo_str = "DIRECIONAL — Sol (L constante)" if modo_direcional else "PONTUAL — Point Light (L por vértice)"
        glfw.set_window_title(window, f"Atividade 7  |  {modo_str}  |  SPACE para alternar")

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_TRIANGLES)
        for tri in triangulos:
            v1, v2, v3 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]
            normal = calcula_normal(v1, v2, v3)
            cor = aplicar_phong(
                normal, v1, pos_camera,
                cor_esfera, brilho,
                modo_direcional, direcao_luz, pos_luz
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
