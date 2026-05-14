import glfw
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
