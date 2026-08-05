import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import sys

# [O dicionário VECTOR_FONT permanece o mesmo do código anterior]
VECTOR_FONT = {
    '0': [((0,0),(1,0)), ((1,0),(1,2)), ((1,2),(0,2)), ((0,2),(0,0))],
    '1': [((0.5,0),(0.5,2))],
    '2': [((0,2),(1,2)), ((1,2),(1,1)), ((1,1),(0,1)), ((0,1),(0,0)), ((0,0),(1,0))],
    '3': [((0,2),(1,2)), ((1,2),(1,1)), ((1,1),(0.2,1)), ((1,1),(1,0)), ((1,0),(0,0))],
    '4': [((0,2),(0,1)), ((0,1),(1,1)), ((1,2),(1,0))],
    '5': [((1,2),(0,2)), ((0,2),(0,1)), ((0,1),(1,1)), ((1,1),(1,0)), ((1,0),(0,0))],
    '6': [((1,2),(0,2)), ((0,2),(0,0)), ((0,0),(1,0)), ((1,0),(1,1)), ((1,1),(0,1))],
    '7': [((0,2),(1,2)), ((1,2),(1,0))],
    '8': [((0,0),(1,0)), ((1,0),(1,2)), ((1,2),(0,2)), ((0,2),(0,0)), ((0,1),(1,1))],
    '9': [((0,0),(1,0)), ((1,0),(1,2)), ((1,2),(0,2)), ((0,2),(0,1)), ((0,1),(1,1))],
    'V': [((0,2),(0.5,0)), ((0.5,0),(1,2))],
    'I': [((0.5,0),(0.5,2)), ((0,0),(1,0)), ((0,2),(1,2))],
    'D': [((0,0),(0,2)), ((0,2),(0.8,2)), ((0.8,2),(1,1)), ((1,1),(0.8,0)), ((0.8,0),(0,0))],
    'A': [((0,0),(0,2)), ((0,2),(1,2)), ((1,2),(1,0)), ((0,1),(1,1))],
    'S': [((1,2),(0,2)), ((0,2),(0,1)), ((0,1),(1,1)), ((1,1),(1,0)), ((1,0),(0,0))],
    'P': [((0,0),(0,2)), ((0,2),(1,2)), ((1,2),(1,1)), ((1,1),(0,1))],
    'T': [((0,2),(1,2)), ((0.5,2),(0.5,0))],
    'E': [((1,2),(0,2)), ((0,2),(0,0)), ((0,0),(1,0)), ((0,1),(0.8,1))],
    'R': [((0,0),(0,2)), ((0,2),(1,2)), ((1,2),(1,1)), ((1,1),(0,1)), ((0,1),(1,0))],
    'O': [((0,0),(1,0)), ((1,0),(1,2)), ((1,2),(0,2)), ((0,2),(0,0))],
    'C': [((1,2),(0,2)), ((0,2),(0,0)), ((0,0),(1,0))],
    'G': [((1,2),(0,2)), ((0,2),(0,0)), ((0,0),(1,0)), ((1,0),(1,1)), ((1,1),(0.5,1))],
    'M': [((0,0),(0,2)), ((0,2),(0.5,1)), ((0.5,1),(1,2)), ((1,2),(1,0))],
    ':': [((0.4,0.4),(0.6,0.4)), ((0.4,0.6),(0.6,0.6)), ((0.4,1.4),(0.6,1.4)), ((0.4,1.6),(0.6,1.6))],
    ' ': []
}

class Game:
    def __init__(self):
        self.player_x = 0.0
        self.player_speed = 9.0
        self.lives = 3
        self.score = 0.0
        self.pyramids = []
        self.spawn_timer = 0.0
        self.spawn_rate = 0.8 
        self.pyramid_speed = 18.0
        self.postes = []
        self.poste_timer = 0.0
        self.poste_rate = 4
        self.is_game_over = False
        self.keys = {glfw.KEY_LEFT: False, glfw.KEY_RIGHT: False}

    def reset(self):
        self.player_x = 0.0
        self.lives = 3
        self.score = 0.0
        self.pyramids.clear()
        self.postes.clear()
        self.is_game_over = False
        self.spawn_rate = 0.8

    def key_callback(self, window, key, scancode, action, mods):
        if key in self.keys:
            if action == glfw.PRESS: self.keys[key] = True
            elif action == glfw.RELEASE: self.keys[key] = False
        if self.is_game_over and action == glfw.PRESS and key == glfw.KEY_ENTER:
            self.reset()

    def update(self, dt):
        if self.is_game_over: return
        self.score += 120 * dt

        if self.keys[glfw.KEY_LEFT]: self.player_x -= self.player_speed * dt
        if self.keys[glfw.KEY_RIGHT]: self.player_x += self.player_speed * dt
        self.player_x = max(-4.0, min(4.0, self.player_x))

        self.poste_timer -= dt
        if self.poste_timer <= 0:
            self.poste_timer = self.poste_rate
            self.postes.append(-60.0)

        for i in range(len(self.postes)-1, -1, -1):
            self.postes[i] += self.pyramid_speed * dt
            if self.postes[i] > 10.0: self.postes.pop(i)

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0.0
            self.pyramids.append([random.uniform(-4.2, 4.2), -60.0])
            if self.spawn_rate > 0.25: self.spawn_rate -= 0.005

        for p in self.pyramids[:]:
            p[1] += self.pyramid_speed * dt 
            if -1.2 < p[1] < 1.2:
                if abs(self.player_x - p[0]) < 1.2: 
                    self.pyramids.remove(p)
                    self.lives -= 1
                    if self.lives <= 0: self.is_game_over = True
            elif p[1] > 10.0:
                self.pyramids.remove(p)

    def draw_cube(self, color):
        vertices = [
            [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
            [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
        ]
        faces = [(0,1,2,3), (3,2,6,7), (7,6,5,4), (4,5,1,0), (5,6,2,1), (7,4,0,3)]
        glColor3fv(color)
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face: glVertex3fv(vertices[vertex])
        glEnd()
        glColor3f(0,0,0); glLineWidth(1.0)
        for face in faces:
            glBegin(GL_LINE_LOOP)
            for v in face: glVertex3fv(vertices[v])
            glEnd()

    def draw_traffic_cone(self):
        # Base Quadrada do Cone
        glPushMatrix()
        glTranslatef(0, -0.1, 0)
        glScalef(0.8, 0.05, 0.8)
        self.draw_cube((1.0, 0.4, 0.0)) # Laranja
        glPopMatrix()

        # Corpo do Cone (Modelado com fatias para parecer circular)
        height = 2.2
        radius = 0.6
        slices = 12
        stacks = 10 # Divisões verticais para criar as listras

        for i in range(stacks):
            y_low = (i / stacks) * height
            y_high = ((i + 1) / stacks) * height
            
            r_low = radius * (1 - (i / stacks))
            r_high = radius * (1 - ((i + 1) / stacks))

            # Lógica da Listra: Se estiver no meio do cone, pinta de branco
            if 3 <= i <= 5: 
                glColor3f(1.0, 1.0, 1.0) # Branco
            else:
                glColor3f(1.0, 0.4, 0.0) # Laranja característico

            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                angle = 2.0 * math.pi * j / slices
                x = math.cos(angle)
                z = math.sin(angle)
                glVertex3f(x * r_low, y_low, z * r_low)
                glVertex3f(x * r_high, y_high, z * r_high)
            glEnd()

    def draw_road(self):
        # Chão cinza escuro
        glColor3f(0.1, 0.1, 0.1)
        glBegin(GL_QUADS)
        glVertex3f(-15.0, -1.0, 10.0); glVertex3f(15.0, -1.0, 10.0)
        glVertex3f(15.0, -1.0, -70.0); glVertex3f(-15.0, -1.0, -70.0)
        glEnd()
        
        # Faixas brancas laterais
        glColor3f(1.0, 0.8, 0.0)
        glBegin(GL_QUADS)
        # Esquerda
        glVertex3f(-5.2, -0.98, 10); glVertex3f(-4.8, -0.98, 10)
        glVertex3f(-4.8, -0.98, -70); glVertex3f(-5.2, -0.98, -70)
        # Direita
        glVertex3f(4.8, -0.98, 10); glVertex3f(5.2, -0.98, 10)
        glVertex3f(5.2, -0.98, -70); glVertex3f(4.8, -0.98, -70)
        glEnd()

    def draw_poste(self):
        glPushMatrix()
        glTranslatef(0.0, 1.5, 0.0); glScalef(0.08, 2.5, 0.08)
        self.draw_cube((0.3, 0.3, 0.3))
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, 4.0, 0.0); glScalef(0.25, 0.1, 0.25)
        self.draw_cube((1.0, 1.0, 0.6)) # Luz amarelada
        glPopMatrix()

    def draw_text_2d(self, text, x, y, size):
        glLineWidth(2.0); glColor3f(1, 1, 1)
        glPushMatrix()
        glTranslatef(x, y, 0); glScalef(size, size, 1)
        for char in text:
            if char in VECTOR_FONT:
                glBegin(GL_LINES)
                for line in VECTOR_FONT[char]:
                    glVertex2f(line[0][0], line[0][1]); glVertex2f(line[1][0], line[1][1])
                glEnd()
            glTranslatef(1.5, 0, 0)
        glPopMatrix()

    def draw_hud(self, width, height):
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
        gluOrtho2D(0, width, 0, height)
        glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        self.draw_text_2d(f"VIDAS: {self.lives}", 20, height - 40, 12)
        score_str = f"SCORE: {int(self.score)}"
        self.draw_text_2d(score_str, width - (len(score_str)*18), height - 40, 12)
        if self.is_game_over:
            self.draw_text_2d("GAME OVER", width/2 - 100, height/2 + 20, 25)
            self.draw_text_2d("PRESS ENTER TO RESTART", width/2 - 160, height/2 - 30, 10)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW); glPopMatrix()

    def draw(self, w, h):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glLoadIdentity()
        gluLookAt(0.0, 3.5, 7.0, 0.0, 1.0, -15.0, 0.0, 1.0, 0.0)
        self.draw_road()
        for z in self.postes:
            for side in [6.5]:
                glPushMatrix(); glTranslatef(side, -1.0, z); self.draw_poste(); glPopMatrix()
        for p in self.pyramids:
            glPushMatrix(); glTranslatef(p[0], -1.0, p[1]); self.draw_traffic_cone(); glPopMatrix()
        glPushMatrix(); glTranslatef(self.player_x, -0.2, 0.0); glScalef(0.7, 0.7, 0.7); self.draw_cube((0.0, 0.6, 1.0)); glPopMatrix()
        self.draw_hud(w, h)

def main():
    if not glfw.init(): return
    w_win, h_win = 900, 700
    window = glfw.create_window(w_win, h_win, "Pirâmides Malditas: Traffic Edition", None, None)
    if not window: glfw.terminate(); return
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.02, 0.02, 0.08, 1.0)
    game = Game()
    glfw.set_key_callback(window, game.key_callback)
    last_time = glfw.get_time()
    while not glfw.window_should_close(window):
        ct = glfw.get_time(); dt = ct - last_time; last_time = ct
        w, h = glfw.get_framebuffer_size(window)
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluPerspective(45, (w/h if h>0 else 1), 0.1, 120.0)
        glMatrixMode(GL_MODELVIEW)
        glfw.poll_events(); game.update(dt); game.draw(w, h)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()