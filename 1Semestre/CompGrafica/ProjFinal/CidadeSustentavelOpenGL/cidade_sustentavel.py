"""
Cidade Sustentavel Interativa

Projeto de Computacao Grafica em OpenGL sem pygame.
O programa cria uma maquete 3D de uma cidade que pode receber melhorias
sustentaveis: arvores, paineis solares, turbinas eolicas, bicicletas e
reducao de fumaca industrial.
"""

import math
import os
import sys
from dataclasses import dataclass

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Erro: instale Pillow com: pip install Pillow")
    raise

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except ImportError:
    print("Erro: instale PyOpenGL com: pip install PyOpenGL PyOpenGL_accelerate")
    raise


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720
TEXTURE_DIR = os.path.join(os.path.dirname(__file__), "textures")
SUN_POSITION = [-18.0, 38.0, 24.0, 1.0]


@dataclass
class GameState:
    money: int = 2600
    time_left: float = 180.0
    trees_planted: int = 0
    solar_panels: int = 0
    wind_turbines: int = 0
    bike_level: int = 0
    anti_smoke_law: bool = False
    pollution: float = 100.0
    game_over: bool = False
    won: bool = False
    message: str = "Ecologize a cidade antes do tempo acabar."
    message_time: float = 4.0


state = GameState()
textures = {}
rendering_shadow = False
camera_x = 0.0
camera_y = 10.0
camera_z = 34.0
camera_yaw = 180.0
camera_pitch = -15.0
mouse_look_active = False
last_mouse_x = 0
last_mouse_y = 0
pressed_keys = set()
last_time = 0
car_offset = 0.0
wind_angle = 0.0
bike_offset = 0.0

TREE_COST = 50
SOLAR_COST = 150
WIND_COST = 300
BIKE_COST = 250
LAW_COST = 400
MAX_TREES = 16
MAX_SOLAR = 8
MAX_WIND = 2
MAX_BIKE_LEVEL = 3
TARGET_SCORE = 85
GAME_DURATION = 180.0


BUILDINGS = [
    (-18, -12, 4, 10, 5), (-10, -12, 5, 14, 4), (8, -12, 5, 12, 5),
    (17, -12, 4, 9, 4), (-18, 10, 4, 8, 5), (-8, 11, 5, 16, 5),
    (9, 11, 4, 11, 5), (18, 10, 5, 13, 4), (-19, -24, 5, 7, 4),
    (-9, -24, 4, 6, 4), (10, -24, 5, 8, 4), (20, -24, 4, 7, 4),
]

BASE_TREES = [
    (-25, 24), (-22, 21), (-18, 24), (-14, 21), (15, 24), (20, 22),
    (24, 25), (-27, -3), (27, -3), (-27, 4), (27, 4),
]

EXTRA_TREES = [
    (-24, 16), (-20, 16), (-16, 16), (-24, 12), (-20, 12), (-16, 12),
    (13, 18), (17, 18), (21, 18), (13, 14), (17, 14), (21, 14),
    (-28, -20), (-25, -17), (25, -18), (28, -21),
]


def create_texture_files():
    os.makedirs(TEXTURE_DIR, exist_ok=True)
    generators = {
        "grass.png": make_grass,
        "road.png": make_road,
        "building.png": make_building,
        "roof.png": make_roof,
        "solar_panel.png": make_solar_panel,
        "leaves.png": make_leaves,
        "smoke.png": make_smoke,
        "water.png": make_water,
    }
    for filename, generator in generators.items():
        path = os.path.join(TEXTURE_DIR, filename)
        if not os.path.exists(path):
            generator(path)


def make_grass(path):
    img = Image.new("RGB", (256, 256), (78, 139, 76))
    draw = ImageDraw.Draw(img)
    for i in range(0, 256, 8):
        color = (60 + (i % 30), 120 + (i % 50), 58)
        draw.line((0, i, 256, i - 30), fill=color, width=2)
    for x in range(0, 256, 16):
        for y in range(0, 256, 16):
            draw.ellipse((x + 4, y + 7, x + 8, y + 11), fill=(100, 166, 86))
    img.save(path)


def make_road(path):
    img = Image.new("RGB", (256, 256), (48, 52, 55))
    draw = ImageDraw.Draw(img)
    for y in range(0, 256, 18):
        draw.line((0, y, 256, y), fill=(57, 61, 64))
    draw.rectangle((120, 0, 136, 256), fill=(230, 209, 92))
    for y in range(0, 256, 44):
        draw.rectangle((123, y, 133, y + 24), fill=(245, 236, 170))
    img.save(path)


def make_building(path):
    img = Image.new("RGB", (256, 256), (110, 122, 132))
    draw = ImageDraw.Draw(img)
    for y in range(18, 250, 42):
        for x in range(20, 236, 46):
            draw.rectangle((x, y, x + 24, y + 22), fill=(174, 207, 218))
            draw.rectangle((x + 3, y + 3, x + 21, y + 19), outline=(214, 235, 240))
    for x in range(0, 256, 64):
        draw.line((x, 0, x, 256), fill=(92, 101, 110), width=3)
    img.save(path)


def make_roof(path):
    img = Image.new("RGB", (256, 256), (135, 74, 58))
    draw = ImageDraw.Draw(img)
    for y in range(0, 256, 32):
        draw.rectangle((0, y, 256, y + 14), fill=(158, 88, 67))
        draw.line((0, y, 256, y), fill=(103, 57, 47), width=2)
    img.save(path)


def make_solar_panel(path):
    img = Image.new("RGB", (256, 256), (13, 31, 54))
    draw = ImageDraw.Draw(img)
    for x in range(20, 240, 44):
        draw.line((x, 12, x, 244), fill=(75, 130, 170), width=3)
    for y in range(20, 240, 44):
        draw.line((12, y, 244, y), fill=(75, 130, 170), width=3)
    draw.rectangle((8, 8, 248, 248), outline=(185, 202, 215), width=8)
    draw.line((30, 40, 150, 10), fill=(135, 190, 225), width=5)
    img.save(path)


def make_leaves(path):
    img = Image.new("RGB", (256, 256), (42, 118, 66))
    draw = ImageDraw.Draw(img)
    for x in range(0, 256, 28):
        for y in range(0, 256, 28):
            draw.ellipse((x, y, x + 34, y + 28), fill=(35 + x % 35, 128 + y % 40, 65))
    img.save(path)


def make_smoke(path):
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    circles = [(70, 165, 70), (120, 120, 86), (165, 85, 62), (98, 70, 48)]
    for cx, cy, r in circles:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(120, 120, 120, 80))
    img.save(path)


def make_water(path):
    img = Image.new("RGB", (256, 256), (54, 132, 160))
    draw = ImageDraw.Draw(img)
    for y in range(16, 256, 30):
        draw.arc((0, y - 18, 100, y + 18), 0, 180, fill=(143, 207, 220), width=3)
        draw.arc((90, y - 18, 210, y + 18), 0, 180, fill=(103, 184, 205), width=3)
    img.save(path)


def load_texture(filename):
    path = os.path.join(TEXTURE_DIR, filename)
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
    mode = GL_RGBA if img.mode == "RGBA" else GL_RGB
    data = img.tobytes()
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, mode, img.width, img.height, mode, GL_UNSIGNED_BYTE, data)
    return tex_id


def init():
    global last_time
    create_texture_files()
    glClearColor(0.55, 0.62, 0.64, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, SUN_POSITION)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.95, 0.9, 0.78, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.35, 0.35, 0.35, 1.0])
    glShadeModel(GL_SMOOTH)
    for name in ("grass", "road", "building", "roof", "solar_panel", "leaves", "smoke", "water"):
        textures[name] = load_texture(name + ".png")
    last_time = glutGet(GLUT_ELAPSED_TIME)


def sustainability_score():
    score = 10
    score += (state.trees_planted / MAX_TREES) * 20
    score += (state.solar_panels / MAX_SOLAR) * 18
    score += (state.wind_turbines / MAX_WIND) * 16
    score += (state.bike_level / MAX_BIKE_LEVEL) * 16
    score += max(0, 30 - state.pollution * 0.3)
    if state.anti_smoke_law:
        score += 5
    return min(100, int(score))


def final_score():
    time_bonus = int(max(0, state.time_left) * 1.5)
    money_bonus = state.money // 10
    return sustainability_score() * 10 + time_bonus + money_bonus


def set_message(text, duration=3.0):
    state.message = text
    state.message_time = duration


def spend_money(cost):
    if state.game_over:
        return False
    if state.money < cost:
        set_message(f"Dinheiro insuficiente. Custo: R$ {cost}.")
        return False
    state.money -= cost
    return True


def plant_tree():
    if state.trees_planted >= MAX_TREES:
        set_message("Todas as areas de plantio ja foram ocupadas.")
        return
    if spend_money(TREE_COST):
        state.trees_planted += 1
        state.pollution = max(0, state.pollution - 1.5)
        set_message(f"Arvore plantada ({state.trees_planted}/{MAX_TREES}).")


def install_solar_panel():
    if state.solar_panels >= MAX_SOLAR:
        set_message("Todos os predios altos ja receberam paineis solares.")
        return
    if spend_money(SOLAR_COST):
        state.solar_panels += 1
        state.pollution = max(0, state.pollution - 2.0)
        set_message(f"Painel solar instalado ({state.solar_panels}/{MAX_SOLAR}).")


def build_wind_turbine():
    if state.wind_turbines >= MAX_WIND:
        set_message("O limite de turbinas eolicas foi atingido.")
        return
    if spend_money(WIND_COST):
        state.wind_turbines += 1
        state.pollution = max(0, state.pollution - 4.0)
        set_message(f"Turbina eolica construida ({state.wind_turbines}/{MAX_WIND}).")


def improve_transport():
    if state.bike_level >= MAX_BIKE_LEVEL:
        set_message("A cidade ja prioriza transporte limpo.")
        return
    if spend_money(BIKE_COST):
        state.bike_level += 1
        state.pollution = max(0, state.pollution - 5.0)
        set_message(f"Ciclovias ampliadas ({state.bike_level}/{MAX_BIKE_LEVEL}).")


def approve_anti_smoke_law():
    if state.anti_smoke_law:
        set_message("A lei antifumaca ja foi aprovada.")
        return
    if spend_money(LAW_COST):
        state.anti_smoke_law = True
        set_message("Lei antifumaca aprovada. A poluicao caira aos poucos.", 4.0)


def reset_game():
    global state, camera_x, camera_y, camera_z, camera_yaw, camera_pitch
    state = GameState()
    camera_x = 0.0
    camera_y = 10.0
    camera_z = 34.0
    camera_yaw = 180.0
    camera_pitch = -15.0
    pressed_keys.clear()


def set_material(r, g, b, alpha=1.0):
    if rendering_shadow:
        glColor4f(0.0, 0.0, 0.0, 0.28)
        return
    glColor4f(r, g, b, alpha)


def bind_texture(name):
    if rendering_shadow:
        glDisable(GL_TEXTURE_2D)
        return
    glBindTexture(GL_TEXTURE_2D, textures[name])


def draw_vertical_cylinder(x, y, z, bottom_radius, top_radius, height, segments=18):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, bottom_radius, top_radius, height, segments, 1)
    glTranslatef(0, 0, height)
    gluDisk(quad, 0, top_radius, segments, 1)
    glPopMatrix()


def draw_textured_box(w, h, d, side_texture="building", top_texture="roof"):
    x, y, z = w / 2, h / 2, d / 2
    bind_texture(side_texture)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0); glVertex3f(-x, -y, z)
    glTexCoord2f(1, 0); glVertex3f(x, -y, z)
    glTexCoord2f(1, 1); glVertex3f(x, y, z)
    glTexCoord2f(0, 1); glVertex3f(-x, y, z)
    glNormal3f(0, 0, -1)
    glTexCoord2f(0, 0); glVertex3f(x, -y, -z)
    glTexCoord2f(1, 0); glVertex3f(-x, -y, -z)
    glTexCoord2f(1, 1); glVertex3f(-x, y, -z)
    glTexCoord2f(0, 1); glVertex3f(x, y, -z)
    glNormal3f(1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(x, -y, z)
    glTexCoord2f(1, 0); glVertex3f(x, -y, -z)
    glTexCoord2f(1, 1); glVertex3f(x, y, -z)
    glTexCoord2f(0, 1); glVertex3f(x, y, z)
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(-x, -y, -z)
    glTexCoord2f(1, 0); glVertex3f(-x, -y, z)
    glTexCoord2f(1, 1); glVertex3f(-x, y, z)
    glTexCoord2f(0, 1); glVertex3f(-x, y, -z)
    glEnd()
    bind_texture(top_texture)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 0); glVertex3f(-x, y, -z)
    glTexCoord2f(1, 0); glVertex3f(x, y, -z)
    glTexCoord2f(1, 1); glVertex3f(x, y, z)
    glTexCoord2f(0, 1); glVertex3f(-x, y, z)
    glEnd()


def draw_textured_plane(size_x, size_z, texture_name, repeat_x=1, repeat_z=1):
    bind_texture(texture_name)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 0); glVertex3f(-size_x / 2, 0, -size_z / 2)
    glTexCoord2f(repeat_x, 0); glVertex3f(size_x / 2, 0, -size_z / 2)
    glTexCoord2f(repeat_x, repeat_z); glVertex3f(size_x / 2, 0, size_z / 2)
    glTexCoord2f(0, repeat_z); glVertex3f(-size_x / 2, 0, size_z / 2)
    glEnd()


def draw_city_base():
    clean_factor = 1.0 - (state.pollution / 100.0)
    sky = 0.52 + clean_factor * 0.32
    glClearColor(0.38 + sky * 0.25, 0.47 + sky * 0.28, 0.55 + sky * 0.35, 1.0)
    set_material(1, 1, 1)
    glPushMatrix()
    draw_textured_plane(64, 64, "grass", 8, 8)
    glPopMatrix()
    set_material(1, 1, 1)
    glPushMatrix()
    glTranslatef(0, 0.03, 0)
    draw_textured_plane(8, 62, "road", 1, 8)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0.04, 0)
    glRotatef(90, 0, 1, 0)
    draw_textured_plane(8, 62, "road", 1, 8)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(22, 0.05, 22)
    set_material(0.8, 0.9, 1.0)
    draw_textured_plane(10, 7, "water", 2, 1)
    glPopMatrix()


def draw_buildings():
    set_material(1.0, 1.0, 1.0)
    solar_drawn = 0
    for x, z, w, h, d in BUILDINGS:
        glPushMatrix()
        glTranslatef(x, h / 2, z)
        draw_textured_box(w, h, d)
        glPopMatrix()
        if h >= 8 and solar_drawn < state.solar_panels:
            draw_solar_panel(x, h + 0.05, z, w * 0.75, d * 0.55)
            solar_drawn += 1


def draw_solar_panel(x, y, z, w, d):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-12, 1, 0, 0)
    set_material(1, 1, 1)
    draw_textured_plane(w, d, "solar_panel", 1, 1)
    glPopMatrix()


def draw_tree(x, z, scale=1.0):
    glPushMatrix()
    glTranslatef(x, 0.05, z)
    glDisable(GL_TEXTURE_2D)
    set_material(0.42, 0.24, 0.12)
    quad = gluNewQuadric()
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 0.22 * scale, 0.16 * scale, 1.7 * scale, 12, 1)
    glPopMatrix()
    glEnable(GL_TEXTURE_2D)
    bind_texture("leaves")
    set_material(0.85, 1.0, 0.85)
    glTranslatef(0, 2.0 * scale, 0)
    leaf_quad = gluNewQuadric()
    gluQuadricTexture(leaf_quad, GL_TRUE)
    gluSphere(leaf_quad, 0.9 * scale, 18, 14)
    glPopMatrix()


def draw_trees():
    for x, z in BASE_TREES:
        draw_tree(x, z, 0.9)
    for x, z in EXTRA_TREES[:state.trees_planted]:
        draw_tree(x, z, 0.9)


def draw_factory():
    glPushMatrix()
    glTranslatef(-24, 2.5, -28)
    set_material(0.65, 0.62, 0.58)
    draw_textured_box(7, 5, 5, "building", "roof")
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)
    set_material(0.32, 0.28, 0.25)
    draw_vertical_cylinder(-26.7, 5.0, -29.1, 0.55, 0.48, 5.4, 20)
    glEnable(GL_TEXTURE_2D)
    if state.pollution > 8 and not rendering_shadow:
        draw_smoke(-26.7, 11, -29.1, state.pollution / 100.0)


def draw_smoke(x, y, z, intensity=1.0):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)
    bind_texture("smoke")
    set_material(1, 1, 1, 0.25 + 0.55 * intensity)
    smoke_layers = 1 + int(intensity * 3)
    for i in range(smoke_layers):
        glPushMatrix()
        glTranslatef(x + i * 0.5, y + i * 1.0, z)
        glRotatef(-camera_yaw, 0, 1, 0)
        size = 3.2 + i * 0.8
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-size / 2, -size / 2, 0)
        glTexCoord2f(1, 0); glVertex3f(size / 2, -size / 2, 0)
        glTexCoord2f(1, 1); glVertex3f(size / 2, size / 2, 0)
        glTexCoord2f(0, 1); glVertex3f(-size / 2, size / 2, 0)
        glEnd()
        glPopMatrix()
    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)


def draw_vehicle(x, z, color, angle=0):
    glPushMatrix()
    glTranslatef(x, 0.55, z)
    glRotatef(angle, 0, 1, 0)
    glDisable(GL_TEXTURE_2D)
    set_material(*color)
    glScalef(1.4, 0.45, 0.8)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(x, 0.9, z)
    glRotatef(angle, 0, 1, 0)
    set_material(0.12, 0.17, 0.2)
    glScalef(0.7, 0.35, 0.65)
    glutSolidCube(1)
    glPopMatrix()
    for dx in (-0.45, 0.45):
        for dz in (-0.38, 0.38):
            glPushMatrix()
            glTranslatef(x + dx * math.cos(math.radians(angle)) - dz * math.sin(math.radians(angle)), 0.28,
                         z + dx * math.sin(math.radians(angle)) + dz * math.cos(math.radians(angle)))
            set_material(0.03, 0.03, 0.03)
            glutSolidSphere(0.16, 10, 8)
            glPopMatrix()
    glEnable(GL_TEXTURE_2D)


def draw_bicycle(x, z, angle=0):
    glPushMatrix()
    glTranslatef(x, 0.42, z)
    glRotatef(angle, 0, 1, 0)
    glDisable(GL_TEXTURE_2D)
    set_material(0.05, 0.05, 0.05)
    for dx in (-0.45, 0.45):
        glPushMatrix()
        glTranslatef(dx, 0, 0)
        glutWireTorus(0.03, 0.22, 8, 16)
        glPopMatrix()
    set_material(0.1, 0.55, 0.85)
    glBegin(GL_LINES)
    glVertex3f(-0.45, 0, 0); glVertex3f(0, 0.45, 0)
    glVertex3f(0.45, 0, 0); glVertex3f(0, 0.45, 0)
    glVertex3f(-0.45, 0, 0); glVertex3f(0.45, 0, 0)
    glEnd()
    glEnable(GL_TEXTURE_2D)
    glPopMatrix()


def draw_transport():
    path = ((car_offset % 52) - 26)
    if state.bike_level >= 3:
        draw_bicycle(path, -2.2, 0)
        draw_bicycle(-path, 2.2, 180)
        draw_bicycle(-2.2, path, -90)
    elif state.bike_level > 0:
        draw_bicycle(path, -2.2, 0)
        draw_vehicle(-path, 2.2, (0.1, 0.2, 0.75), 180)
        if state.bike_level >= 2:
            draw_bicycle(-2.2, path, -90)
        else:
            draw_vehicle(-2.2, path, (0.9, 0.72, 0.1), -90)
    else:
        draw_vehicle(path, -2.2, (0.8, 0.1, 0.08), 0)
        draw_vehicle(-path, 2.2, (0.1, 0.2, 0.75), 180)
        draw_vehicle(-2.2, path, (0.9, 0.72, 0.1), -90)


def draw_wind_turbine(x, z):
    glDisable(GL_TEXTURE_2D)
    glPushMatrix()
    glTranslatef(x, 0, z)
    set_material(0.86, 0.88, 0.86)
    quad = gluNewQuadric()
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 0.22, 0.15, 7.0, 16, 1)
    glPopMatrix()
    glTranslatef(0, 7.0, 0)
    glutSolidSphere(0.32, 14, 10)
    glRotatef(wind_angle, 0, 0, 1)
    set_material(0.95, 0.95, 0.9)
    for angle in (0, 120, 240):
        glPushMatrix()
        glRotatef(angle, 0, 0, 1)
        glTranslatef(0, 1.0, 0)
        glScalef(0.14, 1.8, 0.07)
        glutSolidCube(1)
        glPopMatrix()
    glPopMatrix()
    glEnable(GL_TEXTURE_2D)


def draw_wind_foundation(x, z):
    glDisable(GL_TEXTURE_2D)
    set_material(0.46, 0.48, 0.47)
    glPushMatrix()
    glTranslatef(x, 0.05, z)
    glScalef(3, 0.1, 3)
    glutSolidCube(1)
    glPopMatrix()
    set_material(0.62, 0.65, 0.63)
    glPushMatrix()
    glTranslatef(x, 0.12, z)
    glScalef(2.1, 0.08, 2.1)
    glutSolidCube(1)
    glPopMatrix()
    glEnable(GL_TEXTURE_2D)


def draw_wind_area():
    draw_wind_foundation(-25, 25)
    draw_wind_foundation(-30, 19)
    if state.wind_turbines >= 1:
        draw_wind_turbine(-25, 25)
    if state.wind_turbines >= 2:
        draw_wind_turbine(-30, 19)


def draw_scene():
    draw_city_base()
    draw_shadows()
    draw_buildings()
    draw_factory()
    draw_trees()
    draw_transport()
    draw_wind_area()
    draw_sun()


def draw_sun():
    glPushAttrib(GL_ENABLE_BIT)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glPushMatrix()
    glTranslatef(SUN_POSITION[0], SUN_POSITION[1], SUN_POSITION[2])
    glColor3f(1.0, 0.88, 0.28)
    glutSolidSphere(1.3, 24, 18)
    glPopMatrix()
    glPopAttrib()


def shadow_matrix_for_ground(light):
    lx, ly, lz, lw = light
    # OpenGL recebe matrizes em ordem de colunas.
    return [
        ly, 0.0, 0.0, 0.0,
        -lx, 0.0, -lz, -lw,
        0.0, 0.0, ly, 0.0,
        0.0, 0.0, 0.0, ly,
    ]


def draw_shadow_casters():
    draw_buildings()
    draw_factory()
    draw_trees()
    draw_transport()
    draw_wind_area()


def draw_shadows():
    global rendering_shadow
    rendering_shadow = True
    glPushAttrib(GL_ENABLE_BIT | GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)
    glPushMatrix()
    glTranslatef(0, 0.045, 0)
    glMultMatrixf(shadow_matrix_for_ground(SUN_POSITION))
    draw_shadow_casters()
    glPopMatrix()
    glDepthMask(GL_TRUE)
    glPopAttrib()
    rendering_shadow = False


def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 200)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    yaw = math.radians(camera_yaw)
    pitch = math.radians(camera_pitch)
    direction_x = math.sin(yaw) * math.cos(pitch)
    direction_y = math.sin(pitch)
    direction_z = math.cos(yaw) * math.cos(pitch)
    gluLookAt(camera_x, camera_y, camera_z,
              camera_x + direction_x, camera_y + direction_y, camera_z + direction_z,
              0, 1, 0)


def draw_hud():
    score = sustainability_score()
    minutes = int(state.time_left // 60)
    seconds = int(state.time_left % 60)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    draw_rect(14, WINDOW_HEIGHT - 94, 540, 78, 0.04, 0.07, 0.08, 0.78)
    glColor3f(0.92, 0.98, 0.94)
    draw_string(28, WINDOW_HEIGHT - 42, "Cidade Sustentavel", GLUT_BITMAP_HELVETICA_18)
    glColor3f(0.75, 0.9, 0.82)
    draw_string(28, WINDOW_HEIGHT - 66, f"Meta: atingir {TARGET_SCORE}% de indice ambiental antes do tempo acabar")
    draw_string(28, WINDOW_HEIGHT - 84, "WASD/QE move | Mouse esquerdo mira | R reinicia")

    panel_x = WINDOW_WIDTH - 300
    draw_rect(panel_x, WINDOW_HEIGHT - 166, 286, 150, 0.04, 0.07, 0.08, 0.82)
    glColor3f(0.95, 0.98, 0.92)
    draw_string(panel_x + 16, WINDOW_HEIGHT - 42, f"R$ {state.money}", GLUT_BITMAP_HELVETICA_18)
    glColor3f(0.72, 0.86, 0.78)
    draw_string(panel_x + 16, WINDOW_HEIGHT - 62, "dinheiro disponivel", GLUT_BITMAP_HELVETICA_10)
    glColor3f(0.95, 0.95, 0.9)
    draw_string(panel_x + 16, WINDOW_HEIGHT - 90, f"Tempo: {minutes:02d}:{seconds:02d}", GLUT_BITMAP_HELVETICA_18)
    glColor3f(0.95, 0.76, 0.66)
    draw_string(panel_x + 16, WINDOW_HEIGHT - 120, f"Poluicao: {int(state.pollution)}%", GLUT_BITMAP_HELVETICA_18)
    glColor3f(0.78, 0.88, 0.82)
    draw_string(panel_x + 16, WINDOW_HEIGHT - 146, f"Pontuacao prevista: {final_score()}")

    draw_rect(14, 68, 526, 102, 0.04, 0.07, 0.08, 0.78)
    glColor3f(0.88, 0.95, 0.9)
    draw_string(28, 146, "Acoes", GLUT_BITMAP_HELVETICA_18)
    glColor3f(0.74, 0.86, 0.78)
    draw_string(28, 124, "1 arvore R$50   2 solar R$150   3 eolica R$300")
    draw_string(28, 104, "4 ciclovia R$250   5 lei antifumaca R$400   Espaco ajuda")
    draw_string(28, 84, f"Arvores {state.trees_planted}/{MAX_TREES} | Paineis {state.solar_panels}/{MAX_SOLAR} | Turbinas {state.wind_turbines}/{MAX_WIND} | Ciclovias {state.bike_level}/{MAX_BIKE_LEVEL}")

    status_text = state.message if state.message_time > 0 else "Escolha uma acao sustentavel com as teclas 1 a 5."
    draw_rect(14, 178, 526, 34, 0.02, 0.11, 0.07, 0.82)
    glColor3f(0.88, 1.0, 0.88)
    draw_string(28, 192, status_text)
    if state.game_over:
        draw_rect(WINDOW_WIDTH // 2 - 210, WINDOW_HEIGHT // 2 - 30, 420, 88, 0.02, 0.06, 0.05, 0.88)
        glColor3f(0.9, 1.0, 0.9)
        result = "VITORIA" if state.won else "FIM DE JOGO"
        draw_string(WINDOW_WIDTH // 2 - 58, WINDOW_HEIGHT // 2 + 26, result, GLUT_BITMAP_HELVETICA_18)
        draw_string(WINDOW_WIDTH // 2 - 146, WINDOW_HEIGHT // 2, f"Pontuacao final: {final_score()} | Pressione R para recomecar")

    glColor3f(0.12, 0.12, 0.12)
    glBegin(GL_QUADS)
    glVertex2f(18, 22); glVertex2f(278, 22); glVertex2f(278, 48); glVertex2f(18, 48)
    glEnd()
    glColor3f(0.16, 0.62, 0.28)
    glBegin(GL_QUADS)
    glVertex2f(20, 24); glVertex2f(20 + score * 2.56, 24); glVertex2f(20 + score * 2.56, 46); glVertex2f(20, 46)
    glEnd()
    glColor3f(1, 1, 1)
    draw_string(28, 30, f"Indice ambiental: {score}%")
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)


def draw_rect(x, y, width, height, r, g, b, alpha):
    glColor4f(r, g, b, alpha)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


def draw_string(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_camera()
    glLightfv(GL_LIGHT0, GL_POSITION, SUN_POSITION)
    draw_scene()
    draw_hud()
    glutSwapBuffers()


def reshape(width, height):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH = max(1, width)
    WINDOW_HEIGHT = max(1, height)
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)


def update(_value):
    global camera_x, camera_y, camera_z, last_time, car_offset, wind_angle, bike_offset
    now = glutGet(GLUT_ELAPSED_TIME)
    delta = (now - last_time) / 1000.0
    last_time = now

    yaw = math.radians(camera_yaw)
    forward_x = math.sin(yaw)
    forward_z = math.cos(yaw)
    right_x = -math.cos(yaw)
    right_z = math.sin(yaw)
    move_x = 0.0
    move_z = 0.0
    move_y = 0.0

    if "w" in pressed_keys:
        move_x += forward_x
        move_z += forward_z
    if "s" in pressed_keys:
        move_x -= forward_x
        move_z -= forward_z
    if "a" in pressed_keys:
        move_x -= right_x
        move_z -= right_z
    if "d" in pressed_keys:
        move_x += right_x
        move_z += right_z
    if "q" in pressed_keys:
        move_y += 1.0
    if "e" in pressed_keys:
        move_y -= 1.0

    horizontal_length = math.sqrt(move_x * move_x + move_z * move_z)
    movement_speed = 13.5
    if horizontal_length > 0:
        camera_x += (move_x / horizontal_length) * movement_speed * delta
        camera_z += (move_z / horizontal_length) * movement_speed * delta
    if move_y != 0:
        camera_y = max(2.0, camera_y + move_y * movement_speed * delta)

    if not state.game_over:
        state.time_left = max(0.0, state.time_left - delta)
        state.message_time = max(0.0, state.message_time - delta)
        if state.anti_smoke_law:
            state.pollution = max(0.0, state.pollution - delta * 5.5)
        else:
            state.pollution = min(100.0, state.pollution + delta * 0.25)
        if sustainability_score() >= TARGET_SCORE:
            state.game_over = True
            state.won = True
            set_message(f"Cidade ecologizada! Pontuacao final: {final_score()}", 999)
        elif state.time_left <= 0:
            state.game_over = True
            state.won = False
            set_message(f"Tempo esgotado. Pontuacao final: {final_score()}", 999)

    car_offset += delta * (7.0 if state.bike_level < 3 else 4.0)
    bike_offset += delta * 4.0
    if state.wind_turbines > 0:
        wind_angle = (wind_angle + delta * 190) % 360
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def keyboard(key, _x, _y):
    if key == b"\x1b":
        sys.exit(0)
    key = key.decode("utf-8").lower()
    if key in ("w", "a", "s", "d", "q", "e"):
        pressed_keys.add(key)
    elif key == "1":
        plant_tree()
    elif key == "2":
        install_solar_panel()
    elif key == "3":
        build_wind_turbine()
    elif key == "4":
        improve_transport()
    elif key == "5":
        approve_anti_smoke_law()
    elif key == " ":
        set_message("Use 1 a 5 para aplicar melhorias em etapas.", 3.0)
    elif key == "r":
        reset_game()


def keyboard_up(key, _x, _y):
    key = key.decode("utf-8").lower()
    pressed_keys.discard(key)


def special_keys(key, _x, _y):
    global camera_yaw, camera_pitch
    if key == GLUT_KEY_LEFT:
        camera_yaw -= 4
    elif key == GLUT_KEY_RIGHT:
        camera_yaw += 4
    elif key == GLUT_KEY_UP:
        camera_pitch = min(45, camera_pitch + 3)
    elif key == GLUT_KEY_DOWN:
        camera_pitch = max(-70, camera_pitch - 3)


def mouse(button, button_state, x, y):
    global mouse_look_active, last_mouse_x, last_mouse_y
    if button == GLUT_LEFT_BUTTON:
        mouse_look_active = button_state == GLUT_DOWN
        last_mouse_x = x
        last_mouse_y = y


def mouse_motion(x, y):
    global camera_yaw, camera_pitch, last_mouse_x, last_mouse_y
    if not mouse_look_active:
        return
    sensitivity = 0.25
    dx = x - last_mouse_x
    dy = y - last_mouse_y
    camera_yaw -= dx * sensitivity
    camera_pitch = max(-70, min(45, camera_pitch - dy * sensitivity))
    last_mouse_x = x
    last_mouse_y = y
    glutPostRedisplay()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Cidade Sustentavel Interativa - OpenGL")
    init()
    glutIgnoreKeyRepeat(1)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)
    glutTimerFunc(16, update, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
