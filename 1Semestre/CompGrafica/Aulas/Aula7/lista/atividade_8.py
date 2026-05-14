import glfw
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
