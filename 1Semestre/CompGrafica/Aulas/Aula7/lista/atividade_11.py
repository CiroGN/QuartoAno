import glfw
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
