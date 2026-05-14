import glfw
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
