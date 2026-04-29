import glfw 
from OpenGL.GL import * 
from OpenGL.GLU import * 
 
# --- Variáveis Globais --- 
pos_x = 0.0 
pos_y = 0.0 
fov = 45.0 
angulo_sol = 0.0 
angulo_terra = 0.0 
angulo_orbita = 0.0 
 
def tratar_teclado(window, key, scancode, action, mods): 
    global pos_x, pos_y, fov, angulo_sol, angulo_terra, angulo_orbita 
    passo = 0.1 
    if action == glfw.PRESS or action == glfw.REPEAT: 
        if key == glfw.KEY_LEFT: pos_x -= passo 
        if key == glfw.KEY_RIGHT: pos_x += passo 
        if key == glfw.KEY_UP: pos_y += passo 
        if key == glfw.KEY_DOWN: pos_y -= passo 
        if key == glfw.KEY_W: fov = max(5.0, fov - 2.0) 
        if key == glfw.KEY_S: fov = min(120.0, fov + 2.0) 
        if key == glfw.KEY_A: angulo_sol -= 2.0 
        if key == glfw.KEY_D: angulo_sol += 2.0 
        if key == glfw.KEY_Q: angulo_orbita -= 2.0 
        if key == glfw.KEY_E: angulo_orbita += 2.0 
 
def desenhar_cubo(tamanho, r, g, b): 
    """ Desenha um cubo completo com todas as 6 faces """ 
    glColor3f(r, g, b) 
    glBegin(GL_QUADS) 
     
    # Face Frontal 
    glVertex3f(-tamanho, -tamanho,  tamanho); glVertex3f( tamanho, -tamanho,  tamanho) 
    glVertex3f( tamanho,  tamanho,  tamanho); glVertex3f(-tamanho,  tamanho,  tamanho) 
    # Face Traseira 
    glVertex3f(-tamanho, -tamanho, -tamanho); glVertex3f(-tamanho,  tamanho, -tamanho) 
    glVertex3f( tamanho,  tamanho, -tamanho); glVertex3f( tamanho, -tamanho, -tamanho) 
    # Face Superior 
    glVertex3f(-tamanho,  tamanho, -tamanho); glVertex3f(-tamanho,  tamanho,  tamanho) 
    glVertex3f( tamanho,  tamanho,  tamanho); glVertex3f( tamanho,  tamanho, -tamanho) 
    # Face Inferior 
    glVertex3f(-tamanho, -tamanho, -tamanho); glVertex3f( tamanho, -tamanho, -tamanho) 
    glVertex3f( tamanho, -tamanho,  tamanho); glVertex3f(-tamanho, -tamanho,  tamanho) 
    # Face Direita 
    glVertex3f( tamanho, -tamanho, -tamanho); glVertex3f( tamanho,  tamanho, -tamanho) 
    glVertex3f( tamanho,  tamanho,  tamanho); glVertex3f( tamanho, -tamanho,  tamanho) 
    # Face Esquerda 
    glVertex3f(-tamanho, -tamanho, -tamanho); glVertex3f(-tamanho, -tamanho,  tamanho) 
    glVertex3f(-tamanho,  tamanho,  tamanho); glVertex3f(-tamanho,  tamanho, -tamanho) 
     
    glEnd() 
 
def main(): 
    glfw.init() 
    janela = glfw.create_window(800, 600, "Cubo 3D - Sol e Terra", None, None) 
    glfw.make_context_current(janela) 
    glfw.set_key_callback(janela, tratar_teclado) 
     
    # CRÍTICO: Ativa o teste de profundidade para o cubo parecer sólido 
    glEnable(GL_DEPTH_TEST) 
 
    while not glfw.window_should_close(janela): 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
 
        # Configuração da Projeção 
        glMatrixMode(GL_PROJECTION) 
        glLoadIdentity() 
        gluPerspective(fov, 800/600, 0.1, 100.0) 
         
        glMatrixMode(GL_MODELVIEW) 
        glLoadIdentity() 
        glTranslatef(pos_x, pos_y, -15) # Afastamos mais para ver a órbita 
        # Sequência para criar o Sistema Solar 
        
 # --- SOL --- 
        glPushMatrix() # "Congela a cena" 
        glRotatef(angulo_sol, 0.0, 1.0, 0.0)
        desenhar_cubo(1.5, 1.0, 0.8, 0.0)
        glPopMatrix() # "Volta para a cena" 
 
        # --- TERRA --- 
        glPushMatrix() 
        glRotatef(angulo_orbita, 0.0, 1.0, 0.0)
        glTranslatef(5.0, 0.0, 0.0)
        glRotatef(angulo_terra, 0.0, 1.0, 0.0)
        desenhar_cubo(0.5, 0.0, 0.5, 1.0)
        glPopMatrix()
 
        glfw.swap_buffers(janela) 
        glfw.poll_events() 
 
    glfw.terminate() 
 
main()