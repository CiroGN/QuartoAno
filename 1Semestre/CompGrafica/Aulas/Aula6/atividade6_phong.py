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


# ── Iluminação de Phong com atenuação por distância ───────────────────────────
#
#  NOVIDADE DA ATIVIDADE 6:
#  Fórmula de atenuação clássica:
#
#    atenuacao = 1 / (Kc + Kl * d + Kq * d²)
#
#  onde:
#    d   = distância entre a luz e o vértice
#    Kc  = coeficiente constante  (evita divisão por zero quando d ≈ 0)
#    Kl  = coeficiente linear     (queda suave com a distância)
#    Kq  = coeficiente quadrático (queda mais acentuada em distâncias maiores)
#
#  A intensidade total (difusa + especular) é multiplicada pela atenuação.
#  A componente ambiente NÃO é atenuada — ela simula luz indireta global.

def aplicar_phong(normal, vertice, pos_luz, pos_camera, cor_base, brilho,
                  kc=1.0, kl=0.14, kq=0.07):

    nx, ny, nz = normal

    # Vetor L e distância à luz
    dx = pos_luz[0] - vertice[0]
    dy = pos_luz[1] - vertice[1]
    dz = pos_luz[2] - vertice[2]
    distancia = math.sqrt(dx**2 + dy**2 + dz**2)
    lx, ly, lz = dx/distancia, dy/distancia, dz/distancia

    # Vetor V (superfície → câmera)
    vx = pos_camera[0] - vertice[0]
    vy = pos_camera[1] - vertice[1]
    vz = pos_camera[2] - vertice[2]
    comp_v = math.sqrt(vx**2 + vy**2 + vz**2)
    vx, vy, vz = vx/comp_v, vy/comp_v, vz/comp_v

    # Componentes escalares
    ambiente = 0.1                                      # NÃO atenuada
    dot_nl   = max(0.0, nx*lx + ny*ly + nz*lz)
    difusa   = 0.6 * dot_nl

    rx = 2*dot_nl*nx - lx
    ry = 2*dot_nl*ny - ly
    rz = 2*dot_nl*nz - lz
    dot_rv   = max(0.0, rx*vx + ry*vy + rz*vz)
    especular = 0.5 * (dot_rv ** brilho) if dot_nl > 0 else 0.0

    # Atenuação — cai com o quadrado da distância
    atenuacao = 1.0 / (kc + kl * distancia + kq * distancia ** 2)

    fator = ambiente + atenuacao * (difusa + especular)

    return (
        min(1.0, cor_base[0] * fator),
        min(1.0, cor_base[1] * fator),
        min(1.0, cor_base[2] * fator),
    )


# ── Estado global ─────────────────────────────────────────────────────────────

# Posição inicial da luz
pos_luz = [2.0, 2.0, 2.0]
passo   = 0.1   # deslocamento por tecla


# ── Callback de teclado ───────────────────────────────────────────────────────
#
#  W/S  → afasta / aproxima no eixo Z
#  A/D  → move no eixo X (esquerda / direita)
#  Q/E  → move no eixo Y (baixo / cima)

def key_callback(window, key, scancode, action, mods):
    global pos_luz
    if action in (glfw.PRESS, glfw.REPEAT):
        if key == glfw.KEY_W: pos_luz[2] += passo   # aproxima (z+)
        if key == glfw.KEY_S: pos_luz[2] -= passo   # afasta  (z-)
        if key == glfw.KEY_A: pos_luz[0] -= passo   # esquerda
        if key == glfw.KEY_D: pos_luz[0] += passo   # direita
        if key == glfw.KEY_Q: pos_luz[1] -= passo   # desce
        if key == glfw.KEY_E: pos_luz[1] += passo   # sobe
        dist = math.sqrt(sum(p**2 for p in pos_luz))
        print(f"  Luz: x={pos_luz[0]:+.2f}  y={pos_luz[1]:+.2f}  z={pos_luz[2]:+.2f}"
              f"  |  distância à esfera = {dist:.2f}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Phong + Atenuação | W/S/A/D/Q/E movem a luz", None, None)
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
    cor_esfera = (0.2, 0.6, 1.0)   # azul claro — brilho especular bem visível
    brilho     = 64

    angulo = 0
    glClearColor(0.05, 0.05, 0.08, 1.0)

    print("=" * 55)
    print("  Atividade 6 – Atenuação por distância")
    print("  W / S  → aproxima / afasta a luz no eixo Z")
    print("  A / D  → move a luz para esquerda / direita")
    print("  Q / E  → move a luz para baixo / cima")
    print(f"  Posição inicial da luz: {pos_luz}")
    print("=" * 55)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotatef(20, 1, 0, 0)
        glRotatef(angulo, 0, 1, 0)
        angulo += 0.5

        dist = math.sqrt(sum(p**2 for p in pos_luz))
        glfw.set_window_title(
            window,
            f"Phong + Atenuação  |  luz em {[round(p,1) for p in pos_luz]}"
            f"  |  dist = {dist:.2f}  |  W/S/A/D/Q/E"
        )

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_TRIANGLES)
        for tri in triangulos:
            v1, v2, v3 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]
            normal = calcula_normal(v1, v2, v3)
            cor = aplicar_phong(
                normal, v1, tuple(pos_luz), pos_camera,
                cor_esfera, brilho
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
