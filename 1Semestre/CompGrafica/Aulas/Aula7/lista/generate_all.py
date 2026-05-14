from pathlib import Path
import math

lista_dir = Path(r"c:\Users\cirog\source\QuartoAno\1Semestre\CompGrafica\Aulas\Aula7\lista")
lista_dir.mkdir(parents=True, exist_ok=True)

helpers = '''import numpy as np
from OpenGL.GL import *
import math


def criar_textura_checkerboard(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    check = size // 8
    for i in range(size):
        for j in range(size):
            if ((i // check) + (j // check)) % 2 == 0:
                data[i, j] = [255, 255, 255]
            else:
                data[i, j] = [50, 50, 50]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def criar_textura_atlas(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    cores = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255]]
    tile = size // 3
    for i in range(2):
        for j in range(3):
            idx = i * 3 + j
            if idx < 6:
                x = j * tile
                y = i * tile
                data[y:y+tile, x:x+tile] = cores[idx]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def criar_textura_agua(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            val = int(100 + 50 * math.sin(i * 0.02) * math.cos(j * 0.02))
            data[i, j] = [val // 3, val, 200]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    return tex_id


def criar_textura_terra(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            val = math.sin(i * 0.01) * math.cos(j * 0.01)
            if val > 0.3:
                data[i, j] = [34, 139, 34]
            else:
                data[i, j] = [0, 100, 200]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def criar_textura_nuvens(size=256):
    data = np.zeros((size, size, 4), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            val = int(150 + 100 * math.sin(i * 0.02) * math.cos(j * 0.02))
            data[i, j] = [255, 255, 255, val // 2]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def criar_textura_skybox(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            ratio = i / size
            if ratio < 0.7:
                val = int(135 + 120 * ratio)
                data[i, j] = [val, val, 255]
            else:
                data[i, j] = [139, 90, 43]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def desenhar_cubo_skybox():
    t = 100.0
    glDisable(GL_CULL_FACE)
    glBegin(GL_QUADS)
    faces = [
        ([(0,0,-t,-t,t), (1,0,t,-t,t), (1,1,t,t,t), (0,1,-t,t,t)], (0,0,1)),
        ([(1,0,-t,-t,-t), (1,1,-t,t,-t), (0,1,t,t,-t), (0,0,t,-t,-t)], (0,0,-1)),
        ([(0,1,-t,t,-t), (0,0,-t,t,t), (1,0,t,t,t), (1,1,t,t,-t)], (0,1,0)),
        ([(1,1,-t,-t,-t), (0,1,t,-t,-t), (0,0,t,-t,t), (1,0,-t,-t,t)], (0,-1,0)),
        ([(0,0,t,-t,-t), (0,1,t,t,-t), (1,1,t,t,t), (1,0,t,-t,t)], (1,0,0)),
        ([(1,0,-t,-t,-t), (1,0,-t,-t,t), (0,0,-t,t,t), (0,1,-t,t,-t)], (-1,0,0)),
    ]
    for verts, norm in faces:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()
    glEnable(GL_CULL_FACE)
'''

(lista_dir / 'helpers.py').write_text(helpers)

atividades = {}

atividades[1] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

rx = ry = 0.0
mouse_down = False
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

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def render(texture_id):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glBegin(GL_QUADS)
    for verts, norm in [
        ([(1.0,1.0,-0.5,-0.5,0.5), (3.0,1.0,0.5,-0.5,0.5), (3.0,3.0,0.5,0.5,0.5), (1.0,3.0,-0.5,0.5,0.5)], (0,0,1)),
        ([(3.0,1.0,-0.5,-0.5,-0.5), (3.0,3.0,-0.5,0.5,-0.5), (1.0,3.0,0.5,0.5,-0.5), (1.0,1.0,0.5,-0.5,-0.5)], (0,0,-1)),
        ([(1.0,3.0,-0.5,0.5,-0.5), (1.0,1.0,-0.5,0.5,0.5), (3.0,1.0,0.5,0.5,0.5), (3.0,3.0,0.5,0.5,-0.5)], (0,1,0)),
        ([(3.0,3.0,-0.5,-0.5,-0.5), (1.0,3.0,0.5,-0.5,-0.5), (1.0,1.0,0.5,-0.5,0.5), (3.0,1.0,-0.5,-0.5,0.5)], (0,-1,0)),
        ([(1.0,1.0,0.5,-0.5,-0.5), (1.0,3.0,0.5,0.5,-0.5), (3.0,3.0,0.5,0.5,0.5), (3.0,1.0,0.5,-0.5,0.5)], (1,0,0)),
        ([(3.0,1.0,-0.5,-0.5,-0.5), (3.0,1.0,-0.5,-0.5,0.5), (1.0,1.0,-0.5,0.5,0.5), (1.0,3.0,-0.5,0.5,-0.5)], (-1,0,0)),
    ]:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, 'Atividade 1: Texture Wrapping', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)
    init()
    texture_id = criar_textura_checkerboard()
    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

if __name__ == '__main__':
    main()
'''

atividades[2] = atividades[1].replace("Atividade 1", "Atividade 2")
atividades[3] = atividades[1].replace("GL_REPEAT", "GL_CLAMP_TO_EDGE").replace("Atividade 1", "Atividade 3")

atividades[4] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_atlas

rx = ry = 0.0
mouse_down = False
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

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def render(texture_id):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for verts, norm in [
        ([(0.0,0.0,-0.5,-0.5,0.5), (0.33,0.0,0.5,-0.5,0.5), (0.33,0.5,0.5,0.5,0.5), (0.0,0.5,-0.5,0.5,0.5)], (0,0,1)),
        ([(0.33,0.0,-0.5,-0.5,-0.5), (0.33,0.5,-0.5,0.5,-0.5), (0.66,0.5,0.5,0.5,-0.5), (0.66,0.0,0.5,-0.5,-0.5)], (0,0,-1)),
        ([(0.66,0.0,-0.5,0.5,-0.5), (0.66,0.5,-0.5,0.5,0.5), (1.0,0.5,0.5,0.5,0.5), (1.0,0.0,0.5,0.5,-0.5)], (0,1,0)),
        ([(0.0,0.5,-0.5,-0.5,-0.5), (0.33,0.5,0.5,-0.5,-0.5), (0.33,1.0,0.5,-0.5,0.5), (0.0,1.0,-0.5,-0.5,0.5)], (0,-1,0)),
        ([(0.33,0.5,0.5,-0.5,-0.5), (0.66,0.5,0.5,0.5,-0.5), (0.66,1.0,0.5,0.5,0.5), (0.33,1.0,0.5,-0.5,0.5)], (1,0,0)),
        ([(0.66,0.5,-0.5,-0.5,-0.5), (0.66,1.0,-0.5,-0.5,0.5), (1.0,1.0,-0.5,0.5,0.5), (1.0,0.5,-0.5,0.5,-0.5)], (-1,0,0)),
    ]:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, 'Atividade 4: Texture Atlas', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)
    init()
    texture_id = criar_textura_atlas()
    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

if __name__ == '__main__':
    main()
'''

atividades[5] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

rx = ry = 0.0
mouse_down = False
last_x = last_y = 0.0
filter_mode = GL_LINEAR
texture_id = None

def mouse_button(window, button, action, mods):
    global mouse_down, last_x, last_y, filter_mode, texture_id
    if button == glfw.MOUSE_BUTTON_LEFT:
        mouse_down = action == glfw.PRESS
        if mouse_down:
            last_x, last_y = glfw.get_cursor_pos(window)
    elif button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        filter_mode = GL_NEAREST if filter_mode == GL_LINEAR else GL_LINEAR
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter_mode)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter_mode)

def cursor_pos(window, xpos, ypos):
    global rx, ry, last_x, last_y
    if mouse_down:
        dx = xpos - last_x
        dy = ypos - last_y
        ry += dx * 0.5
        rx += dy * 0.5
        last_x, last_y = xpos, ypos

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for verts, norm in [
        ([(0,0,-0.5,-0.5,0.5), (1,0,0.5,-0.5,0.5), (1,1,0.5,0.5,0.5), (0,1,-0.5,0.5,0.5)], (0,0,1)),
        ([(1,0,-0.5,-0.5,-0.5), (1,1,-0.5,0.5,-0.5), (0,1,0.5,0.5,-0.5), (0,0,0.5,-0.5,-0.5)], (0,0,-1)),
        ([(0,1,-0.5,0.5,-0.5), (0,0,-0.5,0.5,0.5), (1,0,0.5,0.5,0.5), (1,1,0.5,0.5,-0.5)], (0,1,0)),
        ([(1,1,-0.5,-0.5,-0.5), (0,1,0.5,-0.5,-0.5), (0,0,0.5,-0.5,0.5), (1,0,-0.5,-0.5,0.5)], (0,-1,0)),
        ([(0,0,0.5,-0.5,-0.5), (0,1,0.5,0.5,-0.5), (1,1,0.5,0.5,0.5), (1,0,0.5,-0.5,0.5)], (1,0,0)),
        ([(1,0,-0.5,-0.5,-0.5), (1,0,-0.5,-0.5,0.5), (0,0,-0.5,0.5,0.5), (0,1,-0.5,0.5,-0.5)], (-1,0,0)),
    ]:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()

def main():
    global texture_id
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, 'Atividade 5: Filtros', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)
    init()
    texture_id = criar_textura_checkerboard()
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter_mode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter_mode)
    while not glfw.window_should_close(window):
        render()
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

if __name__ == '__main__':
    main()
'''

atividades[6] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

rx = ry = 0.0
zoom_z = -5.0
mouse_down = False
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
    global zoom_z
    zoom_z += yoffset * 0.5
    zoom_z = max(-15.0, min(-2.0, zoom_z))

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def render(texture_id):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, zoom_z)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for verts, norm in [
        ([(0,0,-0.5,-0.5,0.5), (1,0,0.5,-0.5,0.5), (1,1,0.5,0.5,0.5), (0,1,-0.5,0.5,0.5)], (0,0,1)),
        ([(1,0,-0.5,-0.5,-0.5), (1,1,-0.5,0.5,-0.5), (0,1,0.5,0.5,-0.5), (0,0,0.5,-0.5,-0.5)], (0,0,-1)),
        ([(0,1,-0.5,0.5,-0.5), (0,0,-0.5,0.5,0.5), (1,0,0.5,0.5,0.5), (1,1,0.5,0.5,-0.5)], (0,1,0)),
        ([(1,1,-0.5,-0.5,-0.5), (0,1,0.5,-0.5,-0.5), (0,0,0.5,-0.5,0.5), (1,0,-0.5,-0.5,0.5)], (0,-1,0)),
        ([(0,0,0.5,-0.5,-0.5), (0,1,0.5,0.5,-0.5), (1,1,0.5,0.5,0.5), (1,0,0.5,-0.5,0.5)], (1,0,0)),
        ([(1,0,-0.5,-0.5,-0.5), (1,0,-0.5,-0.5,0.5), (0,0,-0.5,0.5,0.5), (0,1,-0.5,0.5,-0.5)], (-1,0,0)),
    ]:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, 'Atividade 6: Zoom com Scroll', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)
    glfw.set_scroll_callback(window, scroll)
    init()
    texture_id = criar_textura_checkerboard()
    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

if __name__ == '__main__':
    main()
'''

atividades[7] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

rx = ry = px = py = 0.0
z = -5.0
left_down = middle_down = False
last_x = last_y = 0.0

def mouse_button(window, button, action, mods):
    global left_down, middle_down, last_x, last_y
    if button == glfw.MOUSE_BUTTON_LEFT:
        left_down = action == glfw.PRESS
    elif button == glfw.MOUSE_BUTTON_MIDDLE:
        middle_down = action == glfw.PRESS
    if action == glfw.PRESS:
        last_x, last_y = glfw.get_cursor_pos(window)

def cursor_pos(window, xpos, ypos):
    global rx, ry, px, py, last_x, last_y
    dx = xpos - last_x
    dy = ypos - last_y
    if left_down:
        ry += dx * 0.5
        rx += dy * 0.5
    elif middle_down:
        px += dx * 0.01
        py -= dy * 0.01
    last_x, last_y = xpos, ypos

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def render(texture_id):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(px, py, z)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for verts, norm in [
        ([(0,0,-0.5,-0.5,0.5), (1,0,0.5,-0.5,0.5), (1,1,0.5,0.5,0.5), (0,1,-0.5,0.5,0.5)], (0,0,1)),
        ([(1,0,-0.5,-0.5,-0.5), (1,1,-0.5,0.5,-0.5), (0,1,0.5,0.5,-0.5), (0,0,0.5,-0.5,-0.5)], (0,0,-1)),
        ([(0,1,-0.5,0.5,-0.5), (0,0,-0.5,0.5,0.5), (1,0,0.5,0.5,0.5), (1,1,0.5,0.5,-0.5)], (0,1,0)),
        ([(1,1,-0.5,-0.5,-0.5), (0,1,0.5,-0.5,-0.5), (0,0,0.5,-0.5,0.5), (1,0,-0.5,-0.5,0.5)], (0,-1,0)),
        ([(0,0,0.5,-0.5,-0.5), (0,1,0.5,0.5,-0.5), (1,1,0.5,0.5,0.5), (1,0,0.5,-0.5,0.5)], (1,0,0)),
        ([(1,0,-0.5,-0.5,-0.5), (1,0,-0.5,-0.5,0.5), (0,0,-0.5,0.5,0.5), (0,1,-0.5,0.5,-0.5)], (-1,0,0)),
    ]:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, 'Atividade 7: Câmera Pan', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)
    init()
    texture_id = criar_textura_checkerboard()
    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

if __name__ == '__main__':
    main()
'''

atividades[8] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_terra

light_x = light_y = 0.0

def cursor_pos(window, xpos, ypos):
    global light_x, light_y
    light_x = (xpos / 800.0) * 8.0 - 4.0
    light_y = -((ypos / 600.0) * 6.0 - 3.0)

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.1, 0.1, 0.1, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLight(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))
    glLight(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

def render(texture_id):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glLight(GL_LIGHT0, GL_POSITION, (light_x, light_y, 3, 1))
    glBindTexture(GL_TEXTURE_2D, texture_id)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 1.0, 32, 32)

if not glfw.init():
    raise SystemExit
window = glfw.create_window(800, 600, 'Atividade 8: Spotlight Móvel', None, None)
if not window:
    glfw.terminate(); raise SystemExit
glfw.make_context_current(window)
glfw.set_cursor_pos_callback(window, cursor_pos)
init()
texture_id = criar_textura_terra()
while not glfw.window_should_close(window):
    render(texture_id)
    glfw.swap_buffers(window)
    glfw.poll_events()
glfw.terminate()
'''

atividades[9] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_checkerboard

rx = ry = 0.0
camera_z = -5.0
target_z = -5.0
last_click = 0.0
mouse_down = False
last_x = last_y = 0.0

def mouse_button(window, button, action, mods):
    global mouse_down, last_x, last_y, last_click, target_z
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            current = glfw.get_time()
            if current - last_click < 0.3:
                target_z = -2.0 if target_z == -5.0 else -5.0
            last_click = current
            mouse_down = True
            last_x, last_y = glfw.get_cursor_pos(window)
        else:
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
    glClearColor(0.2, 0.2, 0.2, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def render(texture_id):
    global camera_z
    camera_z += (target_z - camera_z) * 0.05
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, camera_z)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for verts, norm in [
        ([(0,0,-0.5,-0.5,0.5), (1,0,0.5,-0.5,0.5), (1,1,0.5,0.5,0.5), (0,1,-0.5,0.5,0.5)], (0,0,1)),
        ([(1,0,-0.5,-0.5,-0.5), (1,1,-0.5,0.5,-0.5), (0,1,0.5,0.5,-0.5), (0,0,0.5,-0.5,-0.5)], (0,0,-1)),
        ([(0,1,-0.5,0.5,-0.5), (0,0,-0.5,0.5,0.5), (1,0,0.5,0.5,0.5), (1,1,0.5,0.5,-0.5)], (0,1,0)),
        ([(1,1,-0.5,-0.5,-0.5), (0,1,0.5,-0.5,-0.5), (0,0,0.5,-0.5,0.5), (1,0,-0.5,-0.5,0.5)], (0,-1,0)),
        ([(0,0,0.5,-0.5,-0.5), (0,1,0.5,0.5,-0.5), (1,1,0.5,0.5,0.5), (1,0,0.5,-0.5,0.5)], (1,0,0)),
        ([(1,0,-0.5,-0.5,-0.5), (1,0,-0.5,-0.5,0.5), (0,0,-0.5,0.5,0.5), (0,1,-0.5,0.5,-0.5)], (-1,0,0)),
    ]:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, 'Atividade 9: Double Click Zoom', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_cursor_pos_callback(window, cursor_pos)
    init()
    texture_id = criar_textura_checkerboard()
    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

if __name__ == '__main__':
    main()
'''

atividades[10] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_agua

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.2, 0.2, 0.3, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def render(texture_id):
    desplazamento = glfw.get_time() * 0.5
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, -1, -8)
    glRotatef(45, 1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glTexCoord2f(0 + desplazamento, 0); glVertex3f(-3, 0, 3)
    glTexCoord2f(3 + desplazamento, 0); glVertex3f(3, 0, 3)
    glTexCoord2f(3 + desplazamento, 3); glVertex3f(3, 0, -3)
    glTexCoord2f(0 + desplazamento, 3); glVertex3f(-3, 0, -3)
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, 'Atividade 10: Animação UV', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    init()
    texture_id = criar_textura_agua()
    while not glfw.window_should_close(window):
        render(texture_id)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

if __name__ == '__main__':
    main()
'''

atividades[11] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_terra, criar_textura_nuvens

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.1, 0.1, 0.2, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLight(GL_LIGHT0, GL_POSITION, (5, 5, 5, 0))
    glLight(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1))

def render(texture_terra, texture_nuvens):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    tempo = glfw.get_time()
    roterra = tempo * 20
    ronuves = tempo * 5
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_terra)
    glPushMatrix()
    glRotatef(roterra, 0, 1, 0)
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluQuadricTexture(q, GL_TRUE)
    gluSphere(q, 1.0, 32, 32)
    glPopMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBindTexture(GL_TEXTURE_2D, texture_nuvens)
    glPushMatrix()
    glRotatef(ronuves, 0, 1, 0)
    q2 = gluNewQuadric()
    gluQuadricNormals(q2, GLU_SMOOTH)
    gluQuadricTexture(q2, GL_TRUE)
    gluSphere(q2, 1.01, 32, 32)
    glPopMatrix()
    glDisable(GL_BLEND)

if not glfw.init():
    raise SystemExit
window = glfw.create_window(800, 600, 'Atividade 11: Terra e Nuvens', None, None)
if not window:
    glfw.terminate(); raise SystemExit
glfw.make_context_current(window)
init()
tex_terra = criar_textura_terra()
tex_nuvens = criar_textura_nuvens()
while not glfw.window_should_close(window):
    render(tex_terra, tex_nuvens)
    glfw.swap_buffers(window)
    glfw.poll_events()
glfw.terminate()
'''

atividades[12] = '''import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import criar_textura_skybox, desenhar_cubo_skybox

rx = ry = 0.0
mouse_down = False
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
        ry += dx * 0.5
        rx += dy * 0.5
        last_x, last_y = xpos, ypos

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.1, 0.1, 0.1, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 500)
    glMatrixMode(GL_MODELVIEW)

def render(texture_id):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glDepthMask(GL_FALSE)
    glPushMatrix()
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    desenhar_cubo_skybox()
    glPopMatrix()
    glDepthMask(GL_TRUE)

if not glfw.init():
    raise SystemExit
window = glfw.create_window(800, 600, 'Atividade 12: Skybox', None, None)
if not window:
    glfw.terminate(); raise SystemExit
glfw.make_context_current(window)
glfw.set_mouse_button_callback(window, mouse_button)
glfw.set_cursor_pos_callback(window, cursor_pos)
init()
tex = criar_textura_skybox()
while not glfw.window_should_close(window):
    render(tex)
    glfw.swap_buffers(window)
    glfw.poll_events()
glfw.terminate()
'''

for i in range(1, 13):
    (lista_dir / f'atividade_{i}.py').write_text(atividades[i])

print('✓ helpers.py criado')
for i in range(1, 13):
    print(f'✓ atividade_{i}.py criado')

# Syntax check
import py_compile
for i in range(1, 13):
    py_compile.compile(str(lista_dir / f'atividade_{i}.py'), doraise=True)
print('✓ Compilação sintática concluída para todas as atividades')
