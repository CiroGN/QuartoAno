from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Variáveis globais
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 10
BALL_SPEED_X = 2
BALL_SPEED_Y = 2

# Posições
paddle1_x = WIDTH // 2 - PADDLE_WIDTH // 2
paddle1_y = 50
paddle2_x = WIDTH // 2 - PADDLE_WIDTH // 2
paddle2_y = HEIGHT - 50 - PADDLE_HEIGHT

ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 0
ball_dy = 0

# Pontos
score1 = 0
score2 = 0

# Estado do jogo
game_state = 'menu'  # 'menu', 'waiting', 'playing'
countdown = 3
two_players = False  # Será definido no menu

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def draw_ball(x, y, size):
    glBegin(GL_QUADS)
    glVertex2f(x - size, y - size)
    glVertex2f(x + size, y - size)
    glVertex2f(x + size, y + size)
    glVertex2f(x - size, y + size)
    glEnd()

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def desenhar():
    global paddle1_x, paddle1_y, paddle2_x, paddle2_y, ball_x, ball_y, score1, score2, game_state, countdown

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if game_state == 'menu':
        glColor3f(1.0, 1.0, 1.0)
        draw_text(WIDTH // 2 - 100, HEIGHT // 2 + 50, "Pong Game")
        draw_text(WIDTH // 2 - 150, HEIGHT // 2, "Press 1 for 1 Player")
        draw_text(WIDTH // 2 - 150, HEIGHT // 2 - 30, "Press 2 for 2 Players")
    elif game_state == 'waiting':
        glColor3f(1.0, 1.0, 1.0)
        draw_text(WIDTH // 2 - 50, HEIGHT // 2, f"Starting in {countdown}...")
    else:  # playing
        # Desenhar barras
        glColor3f(1.0, 1.0, 1.0)
        draw_rect(paddle1_x, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        if two_players:
            draw_rect(paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT)

        # Desenhar bola
        glColor3f(1.0, 0.0, 0.0)
        draw_ball(ball_x, ball_y, BALL_SIZE)

        # Desenhar placar
        glColor3f(1.0, 1.0, 1.0)
        draw_text(10, HEIGHT - 30, f"Jogador 1: {score1}")
        if two_players:
            draw_text(WIDTH - 150, HEIGHT - 30, f"Jogador 2: {score2}")

    glutSwapBuffers()

def atualizar(value):
    global ball_x, ball_y, ball_dx, ball_dy, score1, score2, game_state, countdown

    if game_state == 'playing':
        # Mover bola
        ball_x += ball_dx
        ball_y += ball_dy

        # Verificar limites laterais
        if ball_x <= 0 or ball_x >= WIDTH:
            ball_dx *= -1

        # Verificar colisão com raquete inferior
        if ball_y - BALL_SIZE <= paddle1_y + PADDLE_HEIGHT and ball_y + BALL_SIZE >= paddle1_y and ball_dy < 0:
            if paddle1_x <= ball_x <= paddle1_x + PADDLE_WIDTH:
                ball_dy *= -1
                score1 += 1
                ball_dx *= 1.1
                ball_dy *= 1.1

        # Verificar colisão com raquete superior se dois jogadores
        if two_players and ball_y + BALL_SIZE >= paddle2_y and ball_y - BALL_SIZE <= paddle2_y + PADDLE_HEIGHT and ball_dy > 0:
            if paddle2_x <= ball_x <= paddle2_x + PADDLE_WIDTH:
                ball_dy *= -1
                score2 += 1
                ball_dx *= 1.1
                ball_dy *= 1.1

        # Verificar se bola passou pelas raquetes (fim de jogo)
        if ball_y <= 0:
            if two_players:
                print(f"Jogador 2 venceu! Com {score2} pontos.")
            else:
                print(f"Fim de jogo! Pontos: {score1}")
            glutLeaveMainLoop()
        elif two_players and ball_y >= HEIGHT:
            print("Jogador 1 venceu!")
            glutLeaveMainLoop()
        elif not two_players and ball_y >= HEIGHT:
            ball_dy *= -1  # Rebater no topo para um jogador

    glutTimerFunc(16, atualizar, 0)  # ~60 FPS
    glutPostRedisplay()

def teclado(key, x, y):
    global paddle1_x, paddle2_x, game_state, two_players

    if game_state == 'menu':
        if key == b'1':
            two_players = False
            start_waiting()
        elif key == b'2':
            two_players = True
            start_waiting()
    elif game_state == 'playing':
        if key == b'a' and paddle1_x > 0:
            paddle1_x -= 30
        elif key == b'd' and paddle1_x < WIDTH - PADDLE_WIDTH:
            paddle1_x += 30

def teclado_especial(key, x, y):
    global paddle1_x, paddle2_x, game_state, two_players

    if game_state == 'playing':
        if two_players:
            if key == GLUT_KEY_LEFT and paddle2_x > 0:
                paddle2_x -= 30
            elif key == GLUT_KEY_RIGHT and paddle2_x < WIDTH - PADDLE_WIDTH:
                paddle2_x += 30
        else:
            if key == GLUT_KEY_LEFT and paddle1_x > 0:
                paddle1_x -= 30
            elif key == GLUT_KEY_RIGHT and paddle1_x < WIDTH - PADDLE_WIDTH:
                paddle1_x += 30

def start_waiting():
    global game_state, countdown
    game_state = 'waiting'
    countdown = 3
    glutTimerFunc(1000, countdown_timer, 0)

def countdown_timer(value):
    global countdown, game_state, ball_dx, ball_dy
    countdown -= 1
    if countdown > 0:
        glutTimerFunc(1000, countdown_timer, 0)
    else:
        game_state = 'playing'
        ball_dx = BALL_SPEED_X * (1 if random.choice([True, False]) else -1)
        ball_dy = BALL_SPEED_Y * (1 if random.choice([True, False]) else -1)


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH, HEIGHT)
glutCreateWindow(b"Pong Game")
init()
glutDisplayFunc(desenhar)
glutKeyboardFunc(teclado)
glutSpecialFunc(teclado_especial)
glutTimerFunc(0, atualizar, 0)
glutMainLoop()