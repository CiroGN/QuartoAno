import glfw
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
